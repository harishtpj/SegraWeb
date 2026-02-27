from django.urls import path
from api.v1.iot import DisposeWasteView
from api.v1.users import UserListView

urlpatterns = [
    path("v1/iot/dispose/", DisposeWasteView.as_view()),
    path("v1/users/", UserListView.as_view()),
]
