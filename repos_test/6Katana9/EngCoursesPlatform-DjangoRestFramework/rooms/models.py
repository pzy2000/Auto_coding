from django.db import models
from account.models import User

class Room(models.Model):
    title = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length = 100)
    room_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')


    def save(self, *args, **kwargs):
        self.title = self.room_user.full_name
        super().save(*args, **kwargs)