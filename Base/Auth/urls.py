from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from .views import CustomTokenObtainPairView
urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('Service_Register/',views.Serviceregister),
    path('Client_Register/',views.ClientRegistration),
    path('Client_Profile/',views.UserProfile),
    path('Update_Client/',views.UpdateClient),
    path('Update_Service/',views.update_service),
    path('Send_Email_Request/',views.send_password_reset_email),
    path('reset_password/<str:uid64>/<str:token>/',views.reset_password)
    
]