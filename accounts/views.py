from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ecocoins.models import EcoCoinTransaction

@login_required
def dashboard(req):
    transactions = EcoCoinTransaction.objects.filter(user=req.user)
    return render(req, 'dashboard.html', {
        transactions: transactions
    })
