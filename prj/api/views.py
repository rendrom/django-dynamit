from prj.api import serializers, permissions, authenticators
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth import login, logout
from rest_framework.permissions import AllowAny


class UserView(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    model = User

    def get_permissions(self):
        # allow non-authenticated user to create
        return (AllowAny() if self.request.method == 'POST'
                else permissions.IsStaffOrTargetUser()),


class AuthView(APIView):
    authentication_classes = (authenticators.QuietBasicAuthentication,)

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(serializers.UserSerializer(request.user).data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response()
