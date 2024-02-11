from django.shortcuts import render
from .models import service,client,Category
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import CategorySerializer
from rest_framework.response import Response
# Create your views here.
# Reservation etc
@api_view(['GET'])
def All_Categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many=True)
    return Response({"data":serializer.data})