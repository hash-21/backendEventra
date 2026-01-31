from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event
import uuid

User=get_user_model()

# Create your models here.
class Registration(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='registrations')
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='registrations')
    qr_code=models.ImageField(upload_to='qr_codes/',blank=True,null=True)
    registration_code=models.CharField(max_length=50,unique=True,blank=True)
    checked_in=models.BooleanField(default=False)
    checked_in_at=models.DateTimeField(blank=True,null=True)
    registered_at=models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-registered_at']


    def __str__(self):
        return f"{self.user.email} - {self.event.title}"
    
    def save(self,*args,**kwargs):
        if not self.registration_code:
            self.registration_code=str(uuid.uuid4())[:12].upper()
        super().save(*args,**kwargs)