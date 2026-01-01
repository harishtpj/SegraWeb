from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Club(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    members = models.ManyToManyField(User, blank=True)

class EcoDrive(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    participants = models.ManyToManyField(User, blank=True)

    def is_active(self):
        from datetime import date
        return self.start_date <= date.today() <= self.end_date

