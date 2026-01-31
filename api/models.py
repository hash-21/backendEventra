from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    ROLE_CHOICES=[
        ('organizer','Organizer'),
        ('speaker','Speaker'),
        ('attendee','Attendee'),
    ]



    email=models.EmailField(unique=True)
    profile_picture=models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio=models.TextField(blank=True, null=True)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='attendee')
    interests=models.TextField(blank=True, help_text="Comma-separated interests e.g., AI, Web Development, Cloud Computing")

    linkedin_url = models.URLField(blank=True)

    city=models.CharField(max_length=100,blank=True)
    country=models.CharField(max_length=100,blank=True)



    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']

    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    class Meta:
        ordering=['-date_joined']

