from django.db import models

# Create your models here.
class Conversation(models.Model):
    user_message = models.TextField()
    bot_reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_message} | Bot: {self.bot_reply} at {self.timestamp}"