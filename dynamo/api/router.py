from dynamo.api.views import DynamicModelViewSet, DynamicModelFieldViewSet
from dynamo.models import DynamicModel
from dynamo.utils import dynamo_exist
from prj.api.views import UserView
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'dynamicmodel', DynamicModelViewSet)
router.register(r'dynamicmodelfields', DynamicModelFieldViewSet)
router.register(r'users', UserView)

if dynamo_exist():
    for model in DynamicModel.objects.all():
        viewset = model.as_modelviewset()
        router.register(r'%s' % model.name, viewset)