from rest_framework import serializers
from Base.models import service,client
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
class ServiceRegister(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    Cat_id = serializers.CharField(write_only=True) 
    class Meta:
        model = service
        fields = ['Service_name','Adress','email','commerce_number','Cat_id','password']


class ClientRegister(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']

class ServiceProfile(serializers.ModelSerializer):
    class Meta:
        model = service
        fields = ['Service_name','Adress','email','commerce_number','category']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = client
        fields = ['user', 'Profile_pic']



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add custom claims to the token here if needed
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user is None:
            raise AuthenticationFailed("Incorrect username or password")

        # Assuming your user model has 'first_name' and 'last_name' fields
        refresh = self.get_token(user)
        data.pop('refresh', None)
        data.pop('access', None)
        data['user'] = {
            'id': user.id,
            'first_name': user.first_name,  # Corrected field name to 'first_name'
            'last_name': user.last_name,    # Corrected field name to 'last_name'
            'username': user.username,
            'email': user.email,
            'token': str(refresh.access_token)
        }
        data['status'] = True
        return data