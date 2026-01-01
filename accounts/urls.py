from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import dashboard, register
from .forms import StyledLoginForm

urlpatterns = [
    path("login/", 
         LoginView.as_view(
             template_name='registration/login.html',
             authentication_form=StyledLoginForm
         ),
         name='login'
    ),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("dashboard/", dashboard, name="dashboard"),
    path("register/", register, name="register"),
]
