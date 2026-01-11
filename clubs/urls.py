from django.urls import path

from clubs import views

urlpatterns = [
    path("", views.club_list, name="club_list"),
    path("create/", views.club_create, name="club_create"),
    path("<int:pk>/", views.club_detail, name="club_detail"),
    path("<int:pk>/join/", views.club_join, name="club_join"),
    path("<int:pk>/leave/", views.club_leave, name="club_leave"),
    path("<int:pk>/edit/", views.club_edit, name="club_edit"),
    path("<int:pk>/delete/", views.club_delete, name="club_delete"),
    path("<int:pk>/add_member/<int:user_id>/", views.club_add_member, name="club_add_member"),
    path("<int:pk>/remove_member/<int:user_id>/", views.club_remove_member, name="club_remove_member"),
    path("my_clubs/", views.my_clubs, name="my_clubs"),
]
