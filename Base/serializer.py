from rest_framework import serializers
from .models import Category,Date

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
        fields = ['id','client','service','place']