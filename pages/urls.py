from django.urls import path

from .views import HomePageView, AboutPageView, TrackingView, HotelListView, HotelDetail, CheckInView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("tracking/", TrackingView.as_view(), name="tracking"),
    path("hotel/", HotelListView.as_view(), name="hotel_list"),
    path("hotel/<int:hotel_id>", HotelDetail.as_view(), name="hotel_detail"),
    path("hotel/<int:hotel_id>/<int:room_id", CheckInView.as_view(), name="check_in"),
    path("about/", AboutPageView.as_view(), name="about"),
    
]
