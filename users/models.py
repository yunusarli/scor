from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to="profile_photos",blank=True,null=True)
    controller = models.BooleanField(default=False)
    caretaker = models.BooleanField(default=False)
    auditor = models.BooleanField(default=False)
    company = models.CharField(max_length=255,blank=False,null=True)
    team = models.CharField(max_length=50,blank=False,null=True)
    mission = models.CharField(max_length=50,blank=False,null=True)
    phone = models.CharField(max_length=12,blank=True,null=True)
    project = models.CharField(max_length=255,blank=True,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def is_controller(self):
        return self.controller
    
    @property
    def is_caretaker(self):
        return self.caretaker
    
    @property
    def is_auditor(self):
        return self.auditor 
    