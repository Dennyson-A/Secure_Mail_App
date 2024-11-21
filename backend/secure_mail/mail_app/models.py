from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    encrypted_body = models.TextField(blank=True, null=True)  # Store encrypted body
    file = models.FileField(upload_to='attachments/', blank=True, null=True)  # Secure file storage
    timestamp = models.DateTimeField(auto_now_add=True)
