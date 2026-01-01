from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class EcoCoinTransaction(models.Model):
    WASTE_TYPES = [
            ('plastic', 'Plastic'),
            ('metal', 'Metal'),
            ('bio', 'Biodegradeable'),
            ('ewaste', 'E-Waste'),
    ]        

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coins = models.IntegerField()
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    source = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
