from django.contrib.auth.models import User

# Create your models here.
import os
from django.db import models
from django.utils import timezone
import uuid

def generate_filename(instance, filename):
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    filename, extension = os.path.splitext(filename)
    return f"photos/{timestamp}_{filename}{extension}"

def generate_secret_token():
    return str(uuid.uuid4())










class Photographer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_credentials = models.CharField(max_length=255, default=uuid.uuid4, unique=True)
    secret_token = models.CharField(max_length=255, default=generate_secret_token, unique=True)
    created =models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.event_credentials:
            self.event_credentials = str(uuid.uuid4())
        if not self.secret_token:
            self.secret_token = generate_secret_token()
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.event_name

class Folder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length = 255)
    folder_credentials = models.CharField(max_length=255, default=uuid.uuid4, unique=True)
    phone_number = models.CharField(max_length = 15, null = True, blank = True)

    def save(self, *args, **kwargs):
        if not self.folder_credentials:
            self.folder_credentials = str(uuid.uuid4())
        super(Folder, self).save(*args, **kwargs)

class Photo(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(Photographer, on_delete=models.SET_NULL, null=True)

    image = models.ImageField(upload_to=generate_filename)
    guest_name = models.CharField(max_length = 255, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)