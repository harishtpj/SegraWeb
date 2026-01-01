from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ecocoins.models import EcoCoinTransaction

from .forms import CustomUserCreationForm


@login_required
def dashboard(req):
    transactions = EcoCoinTransaction.objects.filter(user=req.user)
    return render(req, "dashboard.html", {"transactions": transactions})


def register(req):
    if req.method == "POST":
        form = CustomUserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(req, "registration/register.html", {"form": form})
