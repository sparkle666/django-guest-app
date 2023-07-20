from django.views.generic import TemplateView
from django.views import View
from accounts.models import CustomUser
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Hotel, Room, Timeline
from faker import Faker
import random
from django.utils import timezone


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"

class TrackingView(View):
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.get(username = request.user.username)
        if user:
            if user.tracking_id is None:
                user.generate_tracking_id()
                user.save()
                messages.success(request, "Generated tracking id", extra_tags = "tracking_success")
        return redirect("home")
        # return HttpResponse("User found")

class HotelListView(View):
    
    def get(self, request, *args, **kwargs):
        hotels = Hotel.objects.all()
        return render(request, "pages/hotels.html", {"hotels": hotels})
    
    def post(self, request, *args, **kwargs):
        # return render(request, "pages/hotels.html", {"hotels": hotels})
        query = request.POST.get("query", "")
        search_results = Hotel.objects.filter(name__icontains = query)
        print(search_results)
        return render(request, "pages/hotel_result.html", {"search_results": search_results, "query": query} )
        

class HotelDetail(View):
    
    def get(self, request, *args, **kwargs):
        hotel_id = kwargs.get("hotel_id")
        hotel = get_object_or_404(Hotel, pk = hotel_id)
        rooms = Room.objects.filter(hotel = hotel)
        return render(request, "pages/hotel_detail.html", {"hotel": hotel, "rooms": rooms})
    
class CheckInView(View):
    
    def post(self, request, *args, **kwargs):
        
        already_checked_in = Room.objects.filter(guest = request.user, is_occupied = True).exists()

        if already_checked_in:
            messages.error(request, "You are already checked into a room.")
            return redirect("hotel_list")
        hotel_id = kwargs.get("hotel_id")
        room_id = kwargs.get("room_id")
        
        hotel = get_object_or_404(Hotel, pk = hotel_id)
        room = get_object_or_404(Room, pk = room_id)
        room.guest = request.user
        if room.is_occupied:
            messages.error(request, "This room is currently occupied!!")
            return redirect('hotel_list')
        room.is_occupied = True
        room.save()
        # Create a timeline for the user
        timeline = Timeline(guest = request.user, room = room)
        timeline.save()
        messages.success(request, "You checked into {hotel.name} in {room.id} successfully!")
        return redirect("user_profile")
     
class UserProfileView(View):
    
    def get(self, request, *args, **kwargs):
        guest = get_object_or_404(CustomUser, pk = request.user.id)
        rooms = Room.objects.filter(guest = guest)
        return render(request, "pages/user_profile.html", {"rooms": rooms})
    
class RoomListView(View):
    
    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        return render(request, "pages/room_list.html", {"rooms": rooms})