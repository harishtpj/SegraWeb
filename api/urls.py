from django.urls import path
from api.v1.iot import DisposeWasteView, IdentifyUserView

urlpatterns = [
    path("v1/iot/identify/", IdentifyUserView.as_view()),
    path("v1/iot/dispose/", DisposeWasteView.as_view()),
]
