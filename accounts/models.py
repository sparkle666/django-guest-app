from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    tracking_id = models.CharField(max_length=200)
    is_checked_in = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def generate_tracking_id(self):
        self.tracking_id = uuid.uuid1()
    
    def get_tracking_id(self):
        return self.tracking_id