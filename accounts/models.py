from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid, os

def profile_photo_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('profile_photos/', filename)

class User(AbstractUser):
    ecocoin_balance = models.IntegerField(default = 0)
    trust_score = models.FloatField(default = 1.0)
    profile_photo = models.ImageField(upload_to=profile_photo_upload_to, null=True, blank=True)
