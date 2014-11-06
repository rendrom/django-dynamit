# coding=utf-8
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
from dynamo.utils import unregister_dynamo, reregister_dynamo, unregister_from_rest_router
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.db import router, models, connection
from dynamo import actions, utils
from django.apps import apps
import json

# Create your models here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, SerializerMethodField

DJANGO_FIELD_MAP = {
    'dynamicbooleanfield':          ('django.db.models', 'BooleanField'),
    'dynamiccharfield':             ('django.db.models', 'CharField'),
    'dynamicdatefield':             ('django.db.models', 'DateField'),
    'dynamicdatetimefield':         ('django.db.models', 'DatetimeField'),
    'dynamicintegerfield':          ('django.db.models', 'IntegerField'),
    'dynamicpositiveintegerfield':  ('django.db.models', 'PositiveIntegerField'),
    'dynamictextfield':             ('django.db.models', 'TextField'),
    'dynamictimefield':             ('django.db.models', 'TimeField'),
    'dynamicurlfield':              ('django.db.models', 'UrlField'),
}

DJANGO_FIELD_CHOICES = [
    ('Basic Fields', [(key, value[1]) for key, value in DJANGO_FIELD_MAP.items()])
]


def get_field_choices():
    del DJANGO_FIELD_CHOICES[:]
    DJANGO_FIELD_CHOICES.append(
        ('Basic Fields', [(key, value[1]) for key, value in DJANGO_FIELD_MAP.items()])
    )
    curlabel = None
    curmodels = None
    # TODO: Переделать
    try:
        for c in ContentType.objects.all().order_by('app_label'):
            if c.app_label != curlabel:
                if curlabel is not None:
                    DJANGO_FIELD_CHOICES.append((curlabel.capitalize(), curmodels))
                curlabel = c.app_label
                curmodels = []
            curmodels.append((c.model, c.name.capitalize()))
        DJANGO_FIELD_CHOICES.append((curlabel.capitalize(), curmodels))
    except Exception:
        # ContentTypes aren't available yet, maybe pre-syncdb
        # print "WARNING: ContentType is not availble"
        pass
        
    return DJANGO_FIELD_CHOICES


class DynamicApp(models.Model):
    name = models.SlugField(verbose_name=_('Application Name'),
                            help_text=_('Internal name for this model'),
                            max_length=64, unique=True,
                            null=False, blank=False)
    verbose_name = models.CharField(verbose_name=_('Verbose Name'),
                            help_text=_('Display name for this application'),
                            max_length=128, null=False, blank=False)

    def __unicode__(self):
        return self.verbose_name

    class Meta:
        verbose_name = _('Dynamic Application')


class DynamicModel(models.Model):
    name = models.SlugField(verbose_name=_('Model Name'),
                            help_text=_('Internal name for this model'),
                            max_length=64, null=False, blank=False)
    verbose_name = models.CharField(verbose_name=_('Verbose Name'),
                            help_text=_('Display name for this model'),
                            max_length=128, null=True, blank=True)
    app = models.ForeignKey(DynamicApp, related_name='models',
                            null=False, blank=False)

    def uncache(self):
        '''
        Removes the model this instance represents from Django's cache

        We need to remove the model from the cache whenever we change it
        otherwise it won't have the changes next time it's loaded
        '''
        app_models = apps.all_models[self.app.name]
        if str(self.name) in app_models:
            del app_models[str(self.name.lower())]

    def uni(self):
        unival = []
        for f in self._meta.fields:
            if len(unival) < 3 and f.__class__ is models.CharField:
                unival.append(getattr(self, f.name))
        if len(unival) > 0:
            return u' '.join(unival)
        else:
            return self.verbose_name

    def as_model(self):
        self.uncache()
        attrs = {}

        class Meta:
            app_label = self.app.name
            verbose_name = self.verbose_name
        attrs['Meta'] = Meta
        attrs['__module__'] = 'dynamo.dynamic_apps.%s.models' % self.app.name
        attrs['__unicode__'] = self.uni
        for field in self.fields.all():
            attrs[field.name] = field.as_field()
        model = type(str(self.name), (models.Model,), attrs)

        return model

    def as_modelviewset(self):
        dynamo_model = self.as_model()
        attrs = {'model': dynamo_model, 'serializer_class': self.as_serializer(), 'permission_classes': [AllowAny,]}
        def get_permissions(self):
            return (IsAuthenticated() if self.request.method == 'POST'
                else AllowAny()),
        def list(self, request, *args, **kwargs):
            response = super(self.__class__, self).list(request, *args, **kwargs)
            instance = {}
            meta = {'verbose_name': {}, 'fieldtype': {}}
            for f in dynamo_model._meta.fields:
                meta['verbose_name'][f.name] = f.verbose_name
                meta['fieldtype'][f.name] = f.get_internal_type()
            instance['features'] = response.data

            instance['meta'] = meta
            return Response(instance)
        attrs['get_permissions'] = get_permissions
        attrs['list'] = list
        viewset = type(str('%sViwSet' % self.name), (viewsets.ModelViewSet,), attrs)
        return viewset

    def as_serializer(self):
        attrs = {}
        dynamo_model = self.as_model()
        dynamo_fields = [f.name for f in dynamo_model._meta.fields].append('field_type')

        class Meta:
            model = dynamo_model
            fields = dynamo_fields
        attrs['Meta'] = Meta
        serializer = type(str('%sSerializer' % self.name), (ModelSerializer,), attrs)
        return serializer

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        if not self.verbose_name:
            self.verbose_name = self.name
        using = using or router.db_for_write(self.__class__, instance=self)
        create = False
        old_exist = self.__class__.objects.filter(pk=self.pk).exists()
        model = self.as_model()
        if self.pk is None or not old_exist:
            create = True
        if not create:
            old = self.__class__.objects.filter(pk=self.pk)
            with connection.schema_editor() as schema_editor:
                app_models = apps.all_models[self.app.name]
                if str(old[0].name) in app_models:
                    old_model = app_models[str(old[0].name)]
                    old_db_table = old_model._meta.db_table
                    new_db_table = model._meta.db_table
                    schema_editor.alter_db_table(old_model, old_db_table, new_db_table)
                    unregister_from_rest_router(old_model)
        super(DynamicModel, self).save(force_insert, force_update, using)
        if create:
            actions.create(model, using)
        reregister_dynamo(model)
        # _update_dynamic_field_choices()

    def __unicode__(self):
        return self.verbose_name

    class Meta:
        verbose_name = _('Dynamic Model')
        unique_together = (('app', 'name'),)


@receiver(pre_delete, sender=DynamicModel)
def dynamicmodel_delete(sender, instance, **kwargs):
    model = instance.as_model()
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(model)
    unregister_dynamo(model)


class DynamicModelField(models.Model):
    name = models.SlugField(verbose_name=_('Field Name'),
                            help_text=_('Internal name for this field'),
                            max_length=64, null=False, blank=False)
    verbose_name = models.CharField(verbose_name=_('Verbose Name'),
                            help_text=_('Display name for this field'),
                            max_length=128, null=True, blank=True)
    model = models.ForeignKey(DynamicModel, related_name='fields',
                            null=False, blank=False)
    field_type = models.CharField(verbose_name=_('Field Type'),
                            help_text=_('Field Data Type'),
                            choices=get_field_choices(),
                            max_length=128, null=False, blank=False)
    null = models.BooleanField(verbose_name=_('Null'),
                            help_text=_('Can this field contain null values?'),
                            default=True, null=False, blank=False)
    blank = models.BooleanField(verbose_name=_('Blank'),
                            help_text=_('Can this field contain empty values?'),
                            default=True, null=False, blank=False)
    unique = models.BooleanField(verbose_name=_('Unique'),
                            help_text=_('Restrict this field to unique values'),
                            default=False, null=False, blank=False)
    default = models.CharField(verbose_name=_('Default value'),
                               help_text=_('Default value given to this field when none is provided'),
                               max_length=32, null=True, blank=True)
    help_text = models.CharField(verbose_name=_('Help Text'),
                            help_text=_('Short description of the field\' purpose'),
                            max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = _('Dynamic Model Field')
        unique_together = (('model', 'name'),)
        ordering = ('id',)

    def as_field(self):
        attrs = {
            'verbose_name': self.verbose_name,
            'blank': self.blank,
            'unique': self.unique,
            'help_text': self.help_text,
        }

        if self.default is not None and self.default != '':
            attrs['default'] = self.default

        field_class = None
        if self.field_type in DJANGO_FIELD_MAP:
            module, klass = DJANGO_FIELD_MAP[self.field_type]
            field_class = utils.get_module_attr(module, klass, models.CharField)

        if field_class is None:
            try:
                ctype = ContentType.objects.get(model=self.field_type)
                field_class = models.ForeignKey
                model_def = DynamicModel.objects.get(name__iexact=ctype.model, app__name__iexact=ctype.app_label)
                model_klass = model_def.as_model()
                attrs['to'] = model_klass
                if attrs['to'] is None:
                    del attrs['to']
                    raise Exception('Could not get model class from %s' % ctype.model)
            except Exception, e:
                print "Failed to set foreign key: %s" % e
                field_class = None

        if field_class is None:
            print "No field class found for %s, using CharField as default" % self.field_type
            field_class = models.CharField

        if field_class is models.CharField:
            attrs['max_length'] = 64
        if field_class is models.BooleanField:
            attrs['default'] = len(str(self.default))
        else:
            attrs['null'] = self.null

        f = field_class(**attrs)
        f.column = self.name
        return f

    def delete(self, using=None):
        with connection.schema_editor() as schema_editor:
            model_class = self.model.as_model()
            field = self.as_field()
            schema_editor.remove_field(model_class, field)
        super(DynamicModelField, self).delete(using)
        reregister_dynamo(self.model.as_model())

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        if not self.verbose_name:
            self.verbose_name = self.name
        model_class = self.model.as_model()
        field = self.as_field()
        with connection.schema_editor() as schema_editor:
            create = False
            if self.pk is None or not self.__class__.objects.filter(pk=self.pk).exists():
                create = True
            if create:
                schema_editor.add_field(model_class, field)
            else:
                old = self.__class__.objects.filter(pk=self.pk)
                with connection.schema_editor() as schema_editor:
                    app_models = apps.all_models[self.model.app.name]
                    if str(old[0].model.name) in app_models:
                        old_model = app_models[str(old[0].model.name)]
                        old_fields = old_model._meta.fields
                        old_field, new_field = None, None
                        for f in old_fields:
                            if f.name == old[0].name:
                                old_field = f
                        new_field = field
                        schema_editor.alter_field(old_model, old_field, new_field)
                        unregister_from_rest_router(old_model)

        super(DynamicModelField, self).save(force_insert, force_update, using)
        reregister_dynamo(self.model.as_model())


    def __unicode__(self):
        return self.verbose_name


def _update_dynamic_field_choices():
    print "Updating dynamic field choices..."
    DynamicModelField._meta.get_field_by_name('field_type')[0]._choices = get_field_choices()
