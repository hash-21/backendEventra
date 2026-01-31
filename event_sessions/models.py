from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from events.models import Event
from django.contrib.auth import get_user_model
# Create your models here.

User=get_user_model()


class Session(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE,related_name='sessions')

    title=models.CharField(max_length=200)
    description=models.TextField()
    speaker=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='speaking_sessions',null=True,blank=True)
    speaker_name=models.CharField(max_length=200,blank=True,help_text='Name of the speaker if not a registered user')
    speaker_bio=models.TextField(blank=True)

    start_time=models.TimeField()
    end_time=models.TimeField()

    room=models.CharField(max_length=100,blank=True,help_text="e.g., Room A, Main Hall")
    track=models.CharField(max_length=100,blank=True,help_text="e.g., Technical, Business")


    topics=models.TextField(blank=True,help_text='Comma separated topics')

    max_attendees=models.PositiveIntegerField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    class Meta:
        ordering=['start_time','room']
        indexes=[models.Index(fields=['event','start_time'])]

    def __str__(self):
        return f"{self.title} ({self.event.title})"
        
    def clean(self):
        if self.end_time <= self.start_time:
                raise ValidationError("End time must be after start time.")
            
        if hasattr(self,'event'):

                if self.start_time<self.event.start_time:
                    raise ValidationError("Session start time cannot be before event start time.")
                if self.end_time>self.event.end_time:
                    raise ValidationError("Session end time cannot be after event end time.")
                
    @property
    def duration_minutes(self):
        start=datetime.combine(datetime.today(),self.start_time)
        end=datetime.combine(datetime.today(),self.end_time)
        duration=end-start
        return int(duration.total_seconds()/60)
            

