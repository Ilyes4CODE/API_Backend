from rest_framework import serializers
from .models import Category,Date,service,History

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','category']


class DateSerializer(serializers.ModelSerializer):
    serv_id = serializers.CharField(write_only=True) 
    class Meta:
        model = Date
        fields = ['serv_id']

class GetDate(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ['id','client','service','place','is_completed']

class Getservices(serializers.ModelSerializer):
    class Meta:
        model = service
        fields = ['id','Service_name','category','profile_pic']

#added new
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id','date','client','service']