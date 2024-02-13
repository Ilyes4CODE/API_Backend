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
    email = models.EmailField(max_length=254,null=True)
    commerce_number = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    Qte = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    

class client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Profile_pic = models.ImageField(default='images/default/DefaultPic.png',upload_to='images/Uploaded/Pfp/')

    def __str__(self):
        return self.user.first_name +' '+self.user.last_name
    


class Date(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=True)
    client = models.ForeignKey(client,on_delete=models.CASCADE,null=True)
    service = models.ForeignKey(service,on_delete=models.CASCADE,null=True)
    place = models.IntegerField(null=True)
    def __str__(self):
        return f'{self.client} Book a place in {self.service} at {self.date}'
    