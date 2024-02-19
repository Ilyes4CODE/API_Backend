from django.shortcuts import get_object_or_404
from .models import service,client,Category,Date
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import CategorySerializer,DateSerializer,GetDate
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User 
from drf_spectacular.utils import extend_schema
# Create your views here.
# Reservation etc
@api_view(['GET'])
@extend_schema(responses=CategorySerializer)
def All_Categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many=True)
    return Response({"data":serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@extend_schema(responses=DateSerializer)
def Take_Date(request):
    data = request.data
    serializer = DateSerializer(data=data, many=False)
    if serializer.is_valid():
        service_name = data.get('serv_id')
        if service.objects.filter(Service_name=service_name).exists():
            serv = service.objects.get(Service_name=service_name)
            client_obj = client.objects.get(user=request.user)
            if Date.objects.filter(client=client_obj, service=serv).exists():
                return Response({"error": "You have already booked a date for this service"}, status=status.HTTP_400_BAD_REQUEST)
            places = Date.objects.filter(service=serv).count()
            Date.objects.create(
                client=client_obj,
                service=serv,
                place=places + 1
            )
            serv.Qte += 1
            serv.save()
            return Response({"Data": f"{request.user} Booked A place"})
        else:
            return Response({"error": "Service not found"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@extend_schema(responses=GetDate)
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
def Delete_Date(request, pk):
    # Retrieve the date object to delete
    object_to_delete = get_object_or_404(Date, pk=pk)
    
    # Check if the authenticated user is either the client or the service related to the date
    if request.user == object_to_delete.client.user or request.user == object_to_delete.service.user:
        # If the authenticated user is authorized, proceed with deletion
        higher_places = Date.objects.filter(place__gt=object_to_delete.place)
        
        # Decrease the place for dates with higher places
        for i in higher_places:
            i.place -= 1
            i.save()
        
        # Delete the date object
        object_to_delete.delete()
        
        return Response({"data": "Deleted"}, status=status.HTTP_200_OK)
    else:
        # If the authenticated user is not authorized, return a permission denied response
        return Response({"error": "Permission denied. You are not authorized to delete this date."}, status=status.HTTP_403_FORBIDDEN)
