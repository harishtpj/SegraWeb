from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ecocoin_balance = models.IntegerField(default = 0)
    trust_score = models.FloatField(default = 1.0)
