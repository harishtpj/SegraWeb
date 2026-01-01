from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
from ecocoins.services import credit_ecocoins, can_credit

@csrf_exempt
def credit(req):
    if req.method != 'POST':
        return JsonResponse({
            'error': 'POST only!'
        }, status=400)

        user = User.objects.get(id=req.POST['user_id'])
        coins = int(req.POST['coins'])

        if not can_credit(coins):
            return JsonResponse({
                'error': 'Daily Limit Exceeded'
            }, status=403)

        credit_ecocoins(user, coins, req.POST['waste_type'])
        return JsonResponse({'status': 'success'})
