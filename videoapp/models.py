# models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class ChatFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)



class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification_code')
    code = models.CharField(max_length=6, unique=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def generate_code(self):
        self.code = str(uuid.uuid4().int)[:6]
        self.save()
