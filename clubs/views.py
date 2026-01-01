from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Club


@login_required
def club_list(req):
    clubs = Club.objects.all()
    return render(req, "clubs.html", {"clubs": clubs})


@login_required
def join_club(req, club_id):
    club = get_object_or_404(Club, id=club_id)
    club.members.add(req.user)
    return redirect("clubs")
