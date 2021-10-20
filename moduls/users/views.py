from moduls.users.task import user_email
from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.response import Response
from moduls.users.serializers import CreateUserSerializer, GetIdUserSerializers, UserSerializer, UpdateUserSerializer
from rest_framework.viewsets import ModelViewSet
from moduls.users.permissions import UserPermissions
from rest_framework.response import Response


# Create your views here.

class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermissions,)
    pagination_class = None

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return  GetIdUserSerializers

        if self.request.method == 'POST':
            return CreateUserSerializer

        if self.request.method == 'PATCH':
            return UpdateUserSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer_class()
        serialized = serializer(data=request.data)

        if not serialized.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serialized.errors)
        user_email.apply_async(
            args=[request.data], 
        )
        serialized.save()
        
        return Response(status=status.HTTP_201_CREATED, data=serialized.data)



