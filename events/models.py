from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User=get_user_model()
# Create your models here.
class Event(models.Model):

    CATEGORY_CHOICES=[
         ('technology', 'Technology'),
        ('business', 'Business'),
        ('health', 'Health & Wellness'),
        ('education', 'Education'),
        ('arts', 'Arts & Culture'),
        ('sports', 'Sports & Fitness'),
        ('food', 'Food & Drink'),
        ('music', 'Music'),
        ('other', 'Other'),
    ]

    title=models.CharField(max_length=200)
    description=models.TextField()
    banner_image=models.ImageField(upload_to='events/',null=True,blank=True)

    date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()

    location=models.CharField(max_length=300)
    venue_name=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    country=models.CharField(max_length=100)

    capacity=models.IntegerField(default=100)

    organizer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='organized_events')

    category=models.CharField(max_length=40,choices=CATEGORY_CHOICES,)


    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-date','-start_time']
        indexes=[
            models.Index(fields=['date','category']),
            models.Index(fields=['city','country'])
        ]

    def __str__(self):
        return self.title
    
    @property
    def total_registrations(self):
        return self.registrations.count()
    
    @property
    def is_full(self):
        return self.total_registrations>=self.capacity
    
    @property
    def is_past(self):
        return self.date<timezone.now().date()
    
    @property
    def available_spots(self):
        return max(0,self.capacity-self.total_registrations)


