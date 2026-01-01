from django.urls import path

from .views import club_list, join_club

urlpatterns = [
    path("clubs/", club_list, name="clubs"),
    path("clubs/join/<int:club_id>/", join_club, name="join_club"),
]
