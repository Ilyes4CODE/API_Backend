from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=50)
    def __str__(self):
        return self.category
    
class service(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='Default_pfp.jpg',upload_to='service_pfp/',null=True)
    Service_name = models.CharField(max_length=50)
    Adress = models.CharField(max_length=50)
    email = models.EmailField(max_length=254,null=True)
    commerce_number = models.CharField(max_length=50)
    nbr_guichet = models.IntegerField(null=True)
    average_time_person = models.IntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    Qte = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    

class client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, max_length=50)
    last_name = models.CharField(null=True, max_length=50)
    phone_number = models.CharField(null=True, max_length=50)
    email = models.EmailField(null=True, max_length=254)
    Profile_pic = models.ImageField(default='Default_pfp.jpg',upload_to='updated_pfp/')

    def __str__(self):
        return self.user.first_name +' '+self.user.last_name
    


class Date(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=True)
    client = models.ForeignKey(client,on_delete=models.CASCADE,null=True)
    service = models.ForeignKey(service,on_delete=models.CASCADE,null=True)
    is_completed = models.BooleanField(default=False)
    place = models.IntegerField(null=True)
    def __str__(self):
        return f'{self.client} Book a place in {self.service} at {self.date}'
    