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


class UserFaceEmbedding(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="face_embedding")
    embedding = models.JSONField(help_text="Face embedding vector as a list of floats")
    model_name = models.CharField(max_length=100, default="placeholder-hash-v1")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.model_name})"
