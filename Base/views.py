from django.shortcuts import get_object_or_404
from .models import service,client,Category,Date
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import CategorySerializer,DateSerializer,GetDate
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User 
# Create your views here.
# Reservation etc
@api_view(['GET'])
def All_Categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many=True)
    return Response({"data":serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Take_Date(request):
    data = request.data
    seriailzer = DateSerializer(data=data,many=False)
    if seriailzer.is_valid():
        if service.objects.filter(Service_name=data['serv_id']).exists():
            serv = service.objects.get(Service_name = data['serv_id']).pk
            serv_id = service.objects.get(pk=serv)
            Client = client.objects.get(user=request.user)
            places = Date.objects.filter(service=serv_id).count()
            Date.objects.create(
                client = Client,
                service = serv_id,
                place = places + 1
            )
            serv_id.Qte += 1
            serv_id.save()
            return Response({"Data":f"{request.user} Booked A place"})
        else:
            return Response({"error":"service not found"},status=status.HTTP_400_BAD_REQUEST)
    else :
        return Response(seriailzer.errors)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_related_date(request):
    user = User.objects.get(username=request.user)
    if user.groups.get().name == "Service":
        Serv = service.objects.get(user=request.user)
        objects = Date.objects.filter(service=Serv)
        serializer = GetDate(objects,many=True)
        return Response({"data":serializer.data})
    elif user.groups.get().name == "Client":
        cli = client.objects.get(user=request.user)
        objects = Date.objects.filter(client=cli)
        serializer = GetDate(objects,many=True)
        return Response({"data":serializer.data})
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Delete_Date(request,pk):
    object_to_delete = get_object_or_404(Date,pk=pk)
    higher_places = Date.objects.filter(place__gt = object_to_delete.place)
    for i in higher_places :
        i.place -= 1
        i.save()
    object_to_delete.delete()
    return Response({"data":"Deleted"})
