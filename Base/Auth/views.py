from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from Base.models import service,client,Category
from .serializer import ServiceSerializer,ClientSerializer,ProfileSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group,User
from rest_framework.permissions import IsAuthenticated
@api_view(['POST'])
def ServiceRegistration(request):
    data = request.data
    servicee = ServiceSerializer(data=data,many=False)
    print(data['category_id'])
    if servicee.is_valid():
        print(servicee.data)
        category = Category.objects.get(category=data['category_id']).pk
        id = Category.objects.get(pk=category)
        if not User.objects.filter(username=data['email']).exists():
            user = service.objects.create(
                username = data['email'],
                Service_name = data['Service_name'],
                Adress = data['Adress'],
                password = make_password(data['password']),
                category = id,
                commerce_number = data['commerce_number'],
                email = data['email'],
            )
            group = Group.objects.get(name="Service")
            user.groups.add(group)
            return Response({'Details' : 'Account Created','account' : servicee.data},status=status.HTTP_201_CREATED)
        else : 
            return Response({'Error':'Account Already Exisits'},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(servicee.errors)

@api_view(['POST'])
def ClientRegistration(request):
    data = request.data
    clientt = ClientSerializer(data=data,many=False)
    if clientt.is_valid():
        if not client.objects.filter(username=data['email']).exists() :
            user = client.objects.create(
                username = data['email'],
                password = make_password(data['password']),
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                phone_number = data['phone_number'],
            ) 
            group = Group.objects.get(name="Client")
            user.groups.add(group)
            return Response({"Details" : "client created succesfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"Error" : "Client Already Existed"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(clientt.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfile(request):
    Client_Serializer = ProfileSerializer(request.user)
    return Response(Client_Serializer.data,status=status.HTTP_200_OK)