from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from .models import Club
from .forms import ClubForm

@login_required
def club_list(req):
    clubs = Club.objects.all()
    return render(req, "clubs/club_list.html", {"clubs": clubs})

@login_required
def my_clubs(req):
    clubs = req.user.created_clubs.all()
    return render(req, "clubs/my_clubs.html", {"clubs": clubs})

@login_required
def club_create(req):
    if req.method == "POST":
        form = ClubForm(req.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.created_by = req.user
            club.save()
            club.members.add(req.user)
            return redirect("club_list")
    else:
        form = ClubForm()
    return render(req, "clubs/club_create.html", {"form": form})

@login_required
def club_detail(req, pk):
    club = get_object_or_404(Club, pk=pk)
    is_member = req.user in club.members.all()
    is_admin = req.user == club.created_by
    return render(req, "clubs/club_detail.html", {
        "club": club, 
        "is_member": is_member, 
        "is_admin": is_admin
    })

@login_required
def club_edit(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.user != club.created_by:
        return redirect("club_detail", pk=pk)

    if request.method == "POST":
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            return redirect("club_detail", pk=pk)
    else:
        form = ClubForm(instance=club)

    return render(request, "clubs/club_create.html", {"form": form})

@login_required
def club_delete(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.user == club.created_by:
        club.delete()
    return redirect("club_list")

@login_required
def club_join(req, pk):
    club = get_object_or_404(Club, id=pk)
    club.members.add(req.user)
    return redirect("club_detail", pk=pk)

@login_required
def club_leave(req, pk):
    club = get_object_or_404(Club, id=pk)
    club.members.remove(req.user)
    return redirect("club_detail", pk=pk)

@login_required
def club_add_member(request, pk, user_id):
    club = get_object_or_404(Club, pk=pk)
    if request.user != club.created_by:
        return redirect("club_detail", pk=pk)
    user = get_object_or_404(User, pk=user_id)
    club.members.add(user)
    return redirect("club_detail", pk=pk)


@login_required
def club_remove_member(request, pk, user_id):
    club = get_object_or_404(Club, pk=pk)
    if request.user != club.created_by:
        return redirect("club_detail", pk=pk)
    user = get_object_or_404(User, pk=user_id)
    club.members.remove(user)
    return redirect("club_detail", pk=pk)
