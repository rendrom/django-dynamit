# coding=utf-8
from dynamo.api.serializers import DynamicModelSerializer, DynamicModelFieldSerializer
from dynamo.models import DynamicModel, DynamicModelField
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, HTMLFormRenderer
from rest_framework.response import Response


class DynamicModelViewSet(viewsets.ModelViewSet):
    model = DynamicModel
    serializer_class = DynamicModelSerializer


class DynamicModelFieldViewSet(viewsets.ModelViewSet):

    queryset = DynamicModelField.objects.all()
    serializer_class = DynamicModelFieldSerializer

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

