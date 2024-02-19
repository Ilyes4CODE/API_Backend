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
    
]