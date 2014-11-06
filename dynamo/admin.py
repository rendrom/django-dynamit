from dynamo.models import DynamicApp, DynamicModel, DynamicModelField
from django.contrib import admin
from dynamo.utils import reregister_in_admin, dynamo_exist


class DynamicAppAdmin(admin.ModelAdmin):
    fields = ('name', 'verbose_name')
    search_fields = ('name','verbose_name')
    ordering = ('name',)
    list_display = ('name', 'verbose_name')
admin.site.register(DynamicApp, DynamicAppAdmin)


class ModelFieldInline(admin.TabularInline):
    model = DynamicModelField
    extra = 10


class DynamicModelAdmin(admin.ModelAdmin):
    fields = ('name', 'app', 'verbose_name')
    search_fields = ('name','verbose_name')
    ordering = ('app','name')
    list_display = ('name', 'verbose_name', 'app')
    list_filter = ('app',)
    inlines = [ModelFieldInline]

admin.site.register(DynamicModel, DynamicModelAdmin)


class DynamicModelFieldAdmin(admin.ModelAdmin):
    search_fields = ('name','verbose_name', 'field_type')
    ordering = ('name',)
    list_display = ('name', 'verbose_name', 'model')
    list_filter = ('model',)
#admin.site.register(DynamicModelField, DynamicModelFieldAdmin)


if dynamo_exist():
    for model in DynamicModel.objects.all():
        reregister_in_admin(model.as_model(), admin.ModelAdmin)
