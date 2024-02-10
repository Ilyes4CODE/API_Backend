from rest_framework import serializers
from Base.models import service,client
class ServiceSerializer(serializers.ModelSerializer):
    category_id = serializers.CharField(write_only=True)
    class Meta:
        model = service
        fields = ['email','Service_name','Adress','password','commerce_number','category_id']
        

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = client
        fields = ['first_name','last_name','email','password','phone_number']



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = client
        fields = ['first_name','last_name','email','Profile_pic','phone_number']

class ServiceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = service
        