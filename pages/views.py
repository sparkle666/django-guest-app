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
from accounts.forms import CustomUserChangeForm
import logging


class HomePageView(TemplateView):
    template_name = "pages/home.html"
  
class AboutPageView(TemplateView):
    template_name = "pages/about.html"

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
            print(f"{request.user} is already checked in...")
            messages.error(request, "You are already checked into a room.")
            return redirect("hotel_list")
        hotel_id = kwargs.get("hotel_id")
        room_id = kwargs.get("room_id")
        
        hotel = get_object_or_404(Hotel, pk = hotel_id)
        room = get_object_or_404(Room, pk = room_id)
        room.guest = request.user
        if room.is_occupied:
            print(f"{room.id} is occuppied: {room.is_occupied}")
            messages.error(request, "This room is currently occupied!!")
            return redirect('hotel_list')
        room.is_occupied = True
        room.save()
        # Create a timeline for the user
        timeline = Timeline(guest = request.user, room = room)
        timeline.save()
        messages.success(request, "You checked into {hotel.name} in {room.id} successfully!")
        return redirect("user_profile")

class CheckOutView(View):
    
    def post(self, request, *args, **kwargs):
        room_id = kwargs.get("room_id")
        guest = request.user
        
        # Get room where user is the current user and room is occupied
        try:
            checked_room = get_object_or_404(Room, guest = guest, is_occupied = True)
            checked_room.is_occupied = False
            # Get timeline of that paricular user and room and add a checkout
            user_timeline = get_object_or_404(Timeline, room = checked_room)
            user_timeline.check_out = True
            
            # Save room and timeline to db
            
            checked_room.save()
            user_timeline.save()
            
            return redirect("hotel_list")
            
        except MultipleObjectsReturned:
            messages.error("An error was encountered")
            logging.error("Each user can only check in to 1 room at a time. Multple checked in rooms detected")
            return redirect("hotel_list")
            
        return redirect("hotel_list")
        
        
class UserProfileView(View):
    
    def get(self, request, *args, **kwargs):
        guest = get_object_or_404(CustomUser, pk = request.user.id)
        rooms = Room.objects.filter(guest = guest)
        form = CustomUserChangeForm(instance = guest)
        return render(request, "pages/user_profile.html", {"rooms": rooms, "form": form})
    
class RoomListView(View):
    
    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        return render(request, "pages/room_list.html", {"rooms": rooms})

class TrackUserView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, "pages/track_user.html", {})
    
    def post(self, request, *args, **kwargs):
        tracking_id = request.POST.get("tracking_id")
        
        user = get_object_or_404(CustomUser, tracking_id = tracking_id)
        user_timeline = Timeline.objects.filter(guest = user)
        
        return render(request, "pages/track_user_details.html", {"user_timeline": user_timeline})