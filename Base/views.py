from django.shortcuts import get_object_or_404
from .models import service,client,Category,Date,History
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import CategorySerializer,DateSerializer,GetDate,Getservices,HistorySerializer
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
def Take_Date(request):
    data = request.data
    print(f"------------{request.user}------------")
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
        service_obj = service.objects.get(user=request.user)
        dates = Date.objects.filter(service=service_obj, is_completed=False).order_by('date')
        data = []
        for date in dates:
            serialized_data = GetDate(date).data
            if hasattr(date, 'client'):  # Check if the client field exists
                serialized_data['client'] = date.client.user.first_name + ' ' + date.client.user.last_name  # Add client name
            serialized_data['service'] = service_obj.Service_name  # Add service name
            data.append(serialized_data)
        return Response({"data": data})
    elif user.groups.get().name == "Client":
        client_obj = client.objects.get(user=request.user)
        client_dates = Date.objects.filter(client=client_obj, is_completed=False)
        if client_dates:
            data = []
            for client_date in client_dates:
                num_clients_before = Date.objects.filter(service=client_date.service, place__lt=client_date.place).count()
                serialized_data = GetDate(client_date).data
                serialized_data['clients_before'] = num_clients_before
                serialized_data['service'] = client_date.service.Service_name  # Change to service name
                data.append(serialized_data)
            return Response({"data": data})
        else:
            return Response({"data": "No dates booked for this client."})
    else:
        return Response({"error": "Unauthorized access."})

#new
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_Historic(request):
    user = User.objects.get(username=request.user)
    if user.groups.get().name == 'Service':
        print('service')
        serv = service.objects.get(user=user)
        related_history = History.objects.filter(service=serv)
        if related_history:
            data = []
            for history in related_history:
                serialized_data = HistorySerializer(history).data
                serialized_data['client'] = history.client.user.first_name +' '+history.client.user.last_name
                serialized_data['service'] = history.service.Service_name
                data.append(serialized_data)
            return Response(data, status=status.HTTP_302_FOUND)
        else:
            return Response({"info": "there is no historic"}, status=status.HTTP_404_NOT_FOUND)
    elif user.groups.get().name == "Client":
        print('client')
        cli = client.objects.get(user=user)
        related_history = History.objects.filter(client=cli)
        if related_history:
            data = []
            for history in related_history:
                serialized_data = HistorySerializer(history).data
                serialized_data['client'] = history.client.user.first_name +' '+history.client.user.last_name
                serialized_data['service'] = history.service.Service_name
                data.append(serialized_data)
            return Response(data, status=status.HTTP_302_FOUND)
        else:
            return Response({"info": "there is no historic client"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"info": "unauthorized"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Delete_Date(request, pk):
    object_to_delete = get_object_or_404(Date, pk=pk)
    
    if request.user == object_to_delete.client.user or request.user == object_to_delete.service.user:
        higher_places = Date.objects.filter(place__gt=object_to_delete.place)
        for i in higher_places:
            i.place -= 1
            i.save()
        
        History.objects.create(
            date = object_to_delete.date,
            client = object_to_delete.client,
            service = object_to_delete.service
        )
        object_to_delete.delete()
        
        return Response({"data": "Deleted"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Permission denied. You are not authorized to delete this date."}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def Get_All_Services(request):
    all_services = service.objects.all()
    serializer = Getservices(all_services,many=True)
    return Response({"Data":serializer.data})


@api_view(['GET'])
def searchByCategorie(request):
    category_id = request.query_params.get('category_id')
    if not category_id:
        return Response({"error": "Category ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    category = get_object_or_404(Category, id=category_id)
    services = service.objects.filter(category=category)

    serializer = Getservices(services, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def searchByServiceName(request):
    service_name = request.query_params.get('service_name')
    if not service_name:
        return Response({"error": "Service name is required"}, status=400)

    services = service.objects.filter(Service_name__icontains=service_name)

    serializer = Getservices(services, many=True)
    return Response(serializer.data)