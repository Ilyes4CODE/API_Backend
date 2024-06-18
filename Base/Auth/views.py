from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from Base.models import service,client,Category
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group,User
from rest_framework.permissions import IsAuthenticated
from .serializer import ServiceRegister,ClientRegister,ServiceProfile,ClientSerializer,CustomTokenObtainPairSerializer,UpdateServiceSerializer,PasswordResetSerializer,InputPasswordSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
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
    serializer = ServiceRegister(data=data, many=False)
    
    if serializer.is_valid():
        service_name_exists = service.objects.filter(Service_name=data['Service_name']).exists()
        commerce_number_exists = service.objects.filter(commerce_number=data['commerce_number']).exists()
        
        if not User.objects.filter(email=data['email']).exists():
            if service_name_exists:
                return Response({"Error": "Service name already taken", 'status': False}, status=status.HTTP_400_BAD_REQUEST)
            elif commerce_number_exists:
                return Response({"Error": "Commerce number already taken", 'status': False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create(
                    username=data['email'],
                    password=make_password(data['password']),
                    email=data['email'],
                )
                cat_id = Category.objects.get(category=data["Cat_id"]).pk
                primary = Category.objects.get(pk=cat_id)
                service_obj = service.objects.create(
                    user=user,
                    Service_name=data['Service_name'],
                    Adress=data['Adress'],
                    email=data['email'],
                    commerce_number=data['commerce_number'],
                    average_time_person=data['average_time_person'],
                    nbr_guichet=data['nbr_guichet'],
                    category=primary
                )
                group = Group.objects.get(name="Service")
                user.groups.add(group)
                return Response({"Data": "Account Created Successfully", 'status': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Error": "Account Already Exists", 'status': False}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

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
@permission_classes([IsAuthenticated])
def update_service(request):
    try:
        service_instance = service.objects.get(user=request.user)
    except service.DoesNotExist:
        return Response({"message": "Service not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateServiceSerializer(service_instance, data=request.data, partial=True)
    if serializer.is_valid():
        # Check if the email field has been changed
        if 'email' in serializer.validated_data:
            new_email = serializer.validated_data['email']
            # Update the username with the new email
            request.user.username = new_email
            request.user.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_password_reset_email(request):
    token_generator = PasswordResetTokenGenerator()
    serializer = PasswordResetSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            return Response({"error": "User not found with this email"}, status=status.HTTP_404_NOT_FOUND)
        
        token = token_generator.make_token(user)
        uid64 = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f'http://127.0.0.1:5500/reset_password.html?uid={uid64}&token={token}'

        # Send email function
        send_mail(
            f'Password Reset For {user.username}',
            f'Your verification link is: {reset_url}',
            settings.EMAIL_HOST_USER,  # Use Django settings for sender email
            [email],
            fail_silently=False,
        )
        return Response({"detail": "Password reset email sent successfully."}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def reset_password(request,uid64,token):
    token_generator = PasswordResetTokenGenerator()
    data = request.data
    serializer = InputPasswordSerializer(data=data)
    if serializer.is_valid():
        new_password = serializer.validated_data['password']
        if uid64 and token and new_password:
            try:
                uid = urlsafe_base64_decode(uid64).decode()
                user = User.objects.get(pk=uid)
                if token_generator.check_token(user,token):
                    user.set_password(new_password)
                    user.save()
                    return Response({'detail': 'Password reset successfully.'}, status=status.HTTP_200_OK)
                else :
                    return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                    return Response({'error': 'Invalid user.'}, status=status.HTTP_400_BAD_REQUEST)
    else : 
        return Response(serializer.errors)