from django.db import transaction
from django.db.models import F, Count
from django.utils import timezone
from .models import EcoCoinTransaction
from clubs.models import EcoDrive

DAILY_LIMIT = 20  # Max 20 disposals per day

# Points per waste type (base points)
WASTE_POINTS = {
    'plastic': 10,
    'metal': 15,
    'bio': 5,
    'organic': 5,  # Handle both 'organic' and 'bio'
    'ewaste': 20,
}

def can_credit(user, coins):
    """
    Check if user can make a disposal today.
    Limit: 20 disposals per day (not points).
    No limit during active EcoDrive.
    """
    # Count disposals today
    today_count = EcoCoinTransaction.objects.filter(
            user = user,
            created_at__date = timezone.now().date()
    ).count()

    active_drive = EcoDrive.objects.filter(
            participants = user,
            start_date__lte = timezone.now().date(),
            end_date__gte = timezone.now().date()
    ).exists()

    if active_drive:
        return True

    # Allow if less than 20 disposals today
    return today_count < DAILY_LIMIT

def calculate_points(waste_type, weight=1.0):
    """
    Calculate points based on waste type and optional weight.
    Weight is a multiplier (default 1.0 for single item).
    """
    # Normalize waste type
    waste_type = waste_type.lower().strip()
    
    base_points = WASTE_POINTS.get(waste_type, 0)
    
    # Bonus for larger quantities
    if weight and weight > 1.0:
        base_points = int(base_points * weight)
    
    return base_points

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
