from django.contrib import admin
from .models import Hotel, HotelImage, Room, Timeline

# Register your models here.
admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(Room)
admin.site.register(Timeline)