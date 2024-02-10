from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=50)
    def __str__(self):
        return self.category
    
class service(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    Service_name = models.CharField(max_length=50)
    Adress = models.CharField(max_length=50)
    commerce_number = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user
    

class client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Profile_pic = models.ImageField(default='images/default/DefaultPic.png')
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return self.user
    


class Date(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=True)
    client = models.ManyToManyField(client)
    service = models.ManyToManyField(service)

    def __str__(self):
        return f'{self.client} Book a place in {self.service} at {self.date}'
    