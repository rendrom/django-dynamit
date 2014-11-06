from dynamo.models import DynamicModel, DynamicModelField
from rest_framework import serializers


class DynamicModelFieldSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DynamicModelField


class DynamicModelSerializer(serializers.ModelSerializer):
    fields = serializers.HyperlinkedRelatedField(view_name='dynamicmodelfield-detail', many=True)


    class Meta:
        model = DynamicModel


