from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import EcoCoinTransaction


@login_required
def transactions(req):
    txns = EcoCoinTransaction.objects.filter(user=req.user) \
            .order_by("-created_at")

    return render(req, "transactions.html", {
        "txns": txns
    })
