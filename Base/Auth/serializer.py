from rest_framework import serializers
from Base.models import service,client
from django.contrib.auth.models import User

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