from django.urls import path

from .views import HomePageView, AboutPageView, HotelListView, HotelDetail, CheckInView, UserProfileView
from .views import RoomListView, TrackUserView, CheckOutView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("tracking/", TrackUserView.as_view(), name="track_user"),
    path("user/profile/", UserProfileView.as_view(), name="user_profile"),
    path("hotel/", HotelListView.as_view(), name="hotel_list"),
    path("room/", RoomListView.as_view(), name="room_list"),
    path("hotel/<int:hotel_id>", HotelDetail.as_view(), name="hotel_detail"),
    path("hotel/<int:hotel_id>/<int:room_id>", CheckInView.as_view(), name="check_in"),
    path("hotel/<int:room_id>", CheckOutView.as_view(), name="check_out"),
    path("about/", AboutPageView.as_view(), name="about"),
    
]
