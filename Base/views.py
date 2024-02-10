from django.shortcuts import render
from .models import service,client
from Auth.serializer import ClientSerializer,ServiceSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

# Create your views here.
# Reservation etc