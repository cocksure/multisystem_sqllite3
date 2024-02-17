from django.db import models
from datetime import timedelta
from django.utils import timezone


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField('users.CustomUser', related_name='chat_rooms')

    def __str__(self):
        return self.name

    def get_users_display(self):
        return ', '.join([user.username for user in self.users.all()])


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, related_name='messages')
    sender = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} - {self.message}"

    @property
    def is_recent(self):
        return self.timestamp >= timezone.now() - timedelta(days=30)
