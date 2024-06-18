from rest_framework import serializers
from Base.models import service,client
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
class ServiceRegister(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    Cat_id = serializers.CharField(write_only=True) 
    class Meta:
        model = service
        fields = ['Service_name','Adress','email','commerce_number','nbr_guichet','average_time_person','Cat_id','password']


class ClientRegister(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = client
        fields = ['first_name','last_name','email','password','phone_number']

class ServiceProfile(serializers.ModelSerializer):
    class Meta:
        model = service
        fields = ['Service_name','profile_pic','Adress','email','commerce_number','category','nbr_guichet','average_time_person']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = client
        fields = ['id','first_name','last_name','phone_number','email', 'Profile_pic']

class UpdateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = service
        fields = ['Service_name','Adress','email','commerce_number','profile_pic','nbr_guichet','average_time_person']

    def update(self, instance, validated_data):
        instance.Service_name = validated_data.get('Service_name', instance.Service_name)
        instance.email = validated_data.get('email', instance.email)
        instance.Adress = validated_data.get('Adress', instance.Adress)
        instance.commerce_number = validated_data.get('commerce_number', instance.commerce_number)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.nbr_guichet = validated_data.get('nbr_guichet', instance.nbr_guichet)
        instance.average_time_person = validated_data.get('average_time_person', instance.average_time_person)
        instance.save()
        return instance

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
        # data.pop('refresh', None)
        # data.pop('access', None)
        data['user'] = {
            'id': user.id,
            'first_name': user.first_name,  # Corrected field name to 'first_name'
            'last_name': user.last_name,    # Corrected field name to 'last_name'
            'username': user.username,
            'email': user.email,
            'groups': list(user.groups.values_list('name', flat=True)),
            # 'token': str(refresh.access_token)
        }
        data['status'] = True
        data['Code'] = status.HTTP_200_OK
        return data
    
#added new : 
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class InputPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()