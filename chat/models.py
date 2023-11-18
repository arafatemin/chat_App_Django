import uuid

from django.contrib.auth.models import User
from django.db import models

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_user = models.ForeignKey(User, related_name="first_room", on_delete=models.CASCADE, null=True)
    second_user = models.ForeignKey(User, related_name="second_room", on_delete=models.CASCADE, null=True)


    class Meta:
        ordering = ['-id']




class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    what_is_it = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['created_date']
