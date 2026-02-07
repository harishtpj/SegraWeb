from django.urls import path
from api.v1.iot import IdentifyUserView, DisposeWasteView
from api.v1.users import UserFaceView


urlpatterns = [
    path("v1/iot/identify/", IdentifyUserView.as_view()),
    path("v1/iot/dispose/", DisposeWasteView.as_view()),
    path("v1/users/<int:user_id>/face/", UserFaceView.as_view()),

]
