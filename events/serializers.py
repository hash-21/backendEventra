from datetime import timezone
from rest_framework import serializers
from .models import Event
from api.serializers import UserSerializer 
from django.utils import timezone

class EventSerializer(serializers.ModelSerializer):
    organizer=UserSerializer(read_only=True)
    total_registrations=serializers.ReadOnlyField()
    is_full=serializers.ReadOnlyField()
    is_past=serializers.ReadOnlyField()
    available_spots=serializers.ReadOnlyField()
    is_registered=serializers.SerializerMethodField()

    class Meta:
        model=Event
        fields=[
            'id','title','description','banner_image','date','start_time','end_time','location','venue_name','city','country','capacity','organizer','category','total_registrations','is_full','is_past','available_spots','created_at','updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def is_registered(self,obj):
        request=self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.registrations.filter(user=request.user).exists()
        return False

class EventListSerializer(serializers.ModelSerializer):
    organizer_name=serializers.CharField(source='organizer.full_name',read_only=True)

    class Meta:
        model=Event
        fields = [
            'id', 'title', 'banner_image', 'date', 'start_time', 'end_time',
            'location', 'venue_name', 'city', 'country',
            'category', 'organizer_name',
            'total_registrations', 'capacity', 'is_full', 'is_past']


class EventCreateUpdateSerializer(serializers.ModelSerializer):
     class Meta:
        model=Event
        fields = [
             'title','description', 'banner_image', 'date', 'start_time','end_time',
            'location', 'venue_name', 'city', 'country',
            'category','capacity',]
        
     def validate_date(self,value):
         if value<timezone.now().date():
             raise serializers.ValidationError('Event date cannot be from the past')
         return value
     
     def validate(self,attrs):
         if 'start_time' in attrs and 'end_time' in attrs:
             if attrs['start_time']>=attrs['end_time']:
                raise serializers.ValidationError({
                    'end_time':'End time must be after start time'
                })
         return attrs
         
             
    


  
