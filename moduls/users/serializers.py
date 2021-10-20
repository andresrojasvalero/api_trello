from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'email', 'last_name','username',)

class CreateUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','username', 'password')
    
    def create(self, validated_data):
        user = User.objects.create(
            **validated_data,

        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class UpdateUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)

class GetIdUserSerializers(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')

