from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from Base.models import service,client,Category
from .serializer import ServiceSerializer,ClientSerializer,ProfileSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group,User
from rest_framework.permissions import IsAuthenticated

