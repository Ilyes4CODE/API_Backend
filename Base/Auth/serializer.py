from rest_framework import serializers
from Base.models import service,client
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
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
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email
        }
        data['Status'] = True

        return data