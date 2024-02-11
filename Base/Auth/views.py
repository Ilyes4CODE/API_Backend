from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from Base.models import service,client,Category
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group,User
from rest_framework.permissions import IsAuthenticated
from .serializer import ServiceRegister,ClientRegister,ServiceProfile,ClientSerializer

@api_view(['POST'])
def Serviceregister(request):
    data = request.data
    serializer = ServiceRegister(data=data,many=False)
    cat_id = Category.objects.get(category=data["Cat_id"]).pk
    primary = Category.objects.get(pk=cat_id)
    if serializer.is_valid():
        if not User.objects.filter(email=data['email']).exists():
            user = User.objects.create(
                username = data['email'],
                password = make_password(data['password']),
                email = data['email'],
            )
            service.objects.create(
                user = user,
                Service_name = data['Service_name'],
                Adress = data['Adress'],
                email = data['email'],
                commerce_number = data['commerce_number'],
                category = primary
            )
            group = Group.objects.get(name="Service")
            print(group)
            user.groups.add(group)
            return Response({"Data" :"Account Created Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"Error":"Account Already Existed"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({serializer.errors})
    

@api_view(['POST'])
def ClientRegistration(request):
    data = request.data
    serializer = ClientRegister(data=data,many=False)
    if serializer.is_valid():
        if not User.objects.filter(email=data['email']).exists():
            user = User.objects.create(
                username = data['email'],
                first_name = data['first_name'],
                last_name = data['last_name'],
                password = make_password(data['password']),
                email = data['email']
            )
            client.objects.create(
                user=user
            )
            group = Group.objects.get(name="Client")
            user.groups.add(group)
            return Response({"Data":"Client Created Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"client Already Existed"},status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response({serializer.errors})
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserProfile(request):
    user = User.objects.get(username = request.user)
    if user.groups.filter(name="Service").exists():
        instance = service.objects.get(user=user)
        serializer = ServiceProfile(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif user.groups.filter(name="Client").exists:
        instance = client.objects.get(user=user)
        serilaizer = ClientSerializer(instance)
        return Response(serilaizer.data,status=status.HTTP_200_OK)


