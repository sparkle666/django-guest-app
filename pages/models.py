from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
import uuid
# Create your models here.


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    rating = models.DecimalField(max_digits=1, decimal_places=0, null=True, choices=[(i, i) for i in range(6)])
    price = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    created = models.DateTimeField(auto_now_add=timezone.now())
    featured_image = models.ImageField(upload_to = "images/", blank = True)

    def __str__(self):
        return self.name
    
class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "images/")
    
    def __str__(self):
        return f"Image - {self.id}"
    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    guest = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank = True)
    is_occupied = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add=timezone.now())

    def __str__(self):
        return f"{self.hotel} - {self.id}"

class Timeline(models.Model):
    guest = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    checked_in = models.DateTimeField(auto_now_add=timezone.now)
    checked_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Timeline {str(self.id)} - {self.guest}"

