from django.urls import path
from . import views
urlpatterns = [
    path('All_Categories/',views.All_Categories),
]
