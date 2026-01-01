from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.timezone import now

from ecocoins.models import EcoCoinTransaction
from ecocoins.services import DAILY_LIMIT

from .forms import RegistrationForm

@login_required
def dashboard(req):
    user = req.user

    txns_cnt = EcoCoinTransaction.objects.filter(
            user=user,
            created_at__date=now().date()
            ).count()

    recent_txns = EcoCoinTransaction.objects.filter(user=user) \
            .order_by('-created_at')[:5]

    return render(req, "dashboard.html", {
        'today_count': txns_cnt,
        'daily_limit': DAILY_LIMIT,
        'clubs': user.clubs.all(),
        'txns': recent_txns,
        'trust_score': user.trust_score * 100,
    })

def register(req):
    if req.method == "POST":
        form = RegistrationForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(req, "registration/register.html", {"form": form})
