from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Hotels(models.Model):
    #h_id,h_name,owner ,location,rooms
    name = models.CharField(max_length=30,default="VietNam")
    owner = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50,default="Hotel")
    country = models.CharField(max_length=50,default="VietNam")
    def __str__(self):
        return self.name

class RoomType(models.Model):
    type_name = models.CharField(max_length=200)
    description_room_type = models.TextField()

    def __str__(self):
        return self.type_name
    
class Rooms(models.Model):
    ROOM_STATUS = ( 
        ("1", "Available"), 
        ("2", "Not available"),    
    ) 
    
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    image = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField()
    price = models.IntegerField()
    size = models.IntegerField()
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE)
    status = models.CharField(choices=ROOM_STATUS, max_length=15)
    roomnumber = models.IntegerField()

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type.type_name}"


class Reservation(models.Model):

    check_in = models.DateField(auto_now =False)
    check_out = models.DateField()
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE)
    guest = models.ForeignKey(User, on_delete= models.CASCADE)
    
    booking_id = models.CharField(max_length=100,default="null")
    def __str__(self):
        return self.guest.username
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.TextField(blank=True, null=True)
    sdt = models.IntegerField()
    address = models.CharField(max_length=150)
    def __str__(self):
       return self.user.username
