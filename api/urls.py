from django.urls import path
from api.v1.iot import IdentifyUserView, DisposeWasteView

urlpatterns = [
    path("v1/iot/identify/", IdentifyUserView.as_view()),
    path("v1/iot/dispose/", DisposeWasteView.as_view()),
]
