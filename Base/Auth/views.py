from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from Base.models import service,client,Category
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group,User
from rest_framework.permissions import IsAuthenticated
from .serializer import ServiceRegister,ClientRegister,ServiceProfile,ClientSerializer,CustomTokenObtainPairSerializer,UpdateServiceSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed as e:
            return Response({
                'status': False,
                'message': "Incorrect username or password"
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@extend_schema(responses=ServiceRegister)
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
            return Response({"Data" :"Account Created Successfully",'status':True},status=status.HTTP_201_CREATED)
        else:
            return Response({"Error":"Account Already Existed",'status':False},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({serializer.errors})
    

@api_view(['POST'])
@extend_schema(responses=ClientRegister)
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
                user=user,
                first_name = data['first_name'],
                last_name = data['last_name'],
                phone_number = data['phone_number'],
                email = data['email']
            )
            group = Group.objects.get(name="Client")
            user.groups.add(group)
            return Response({"Data":"Client Created Successfully",'status':True},status=status.HTTP_201_CREATED)
        else:
            return Response({"data":"client Already Existed",'status':False},status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response({serializer.errors})
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@extend_schema(responses=ServiceProfile)
def UserProfile(request):
    user = User.objects.get(username = request.user)
    if user.groups.filter(name="Service").exists():
        instance = service.objects.get(user=user)
        serializer = ServiceProfile(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif user.groups.filter(name="Client").exists():
        instance = client.objects.get(user=user)
        serilaizer = ClientSerializer(instance)
        return Response(serilaizer.data,status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def UpdateClient(request):
    profile = client.objects.get(user=request.user)
    data = request.data
    Serializer = ClientSerializer(instance=profile, data=data, partial=True)
    if Serializer.is_valid():
        if data.get('email', ''):  # check if email field is provided and not empty
            profile.user.username = data['email']
            profile.user.save()
            profile.save()
            Serializer.save()
            updated_profile = ClientSerializer(profile)  # serialize updated profile
            return Response({'info': 'Username and info updated successfully', 'profile': updated_profile.data})
        else:
            Serializer.save()
            updated_profile = ClientSerializer(profile)  # serialize updated profile
            return Response({'info': 'Updated successfully', 'profile': updated_profile.data})
    else:
        return Response(Serializer.errors)
        
@api_view(['PATCH'])
def update_service(request, pk):
    try:
        service_instance = service.objects.get(pk=pk)
    except service.DoesNotExist:
        return Response({"message": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateServiceSerializer(service_instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)