from django.urls import path
from . import views
urlpatterns = [
    path('All_Categories/',views.All_Categories),
    path('RegisterDate/',views.Take_Date),
    path('Related_objects/',views.get_related_date),
    path('Delete_Date/<str:pk>/',views.Delete_Date),
    path('All_Services/',views.Get_All_Services),
    path('Get_Historic/',views.Get_Historic),
    path('Search_By_Category/',views.searchByCategorie),
    path('Search_By_Service_Name/',views.searchByServiceName),
]
