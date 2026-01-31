from django.db import transaction
from django.db.models import F, Sum
from django.utils import timezone
from .models import EcoCoinTransaction
from clubs.models import EcoDrive

DAILY_LIMIT = 20

def can_credit(user, coins):
    today_total = EcoCoinTransaction.objects.filter(
            user = user,
            created_at__date = timezone.now().date()
    ).aggregate(total = Sum('coins'))['total'] or 0

    active_drive = EcoDrive.objects.filter(
            participants = user,
            start_date__lte = timezone.now().date(),
            end_date__gte = timezone.now().date()
    ).exists()

    if active_drive:
        return True

    return today_total + coins <= DAILY_LIMIT

@transaction.atomic
def credit_ecocoins(user, coins, waste_type, source="bin"):
    EcoCoinTransaction.objects.create(
            user = user,
            coins = coins,
            waste_type = waste_type,
            source = source
    )
    user.ecocoin_balance = F('ecocoin_balance') + coins
    user.save(update_fields = ['ecocoin_balance'])
