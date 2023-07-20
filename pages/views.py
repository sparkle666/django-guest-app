from django.views.generic import TemplateView
from django.views import View
from accounts.models import CustomUser
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .models import Hotel, Room
from faker import Faker
import random


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