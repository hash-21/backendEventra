from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Registration
from events.serializers import EventListSerializer
from api.serializers import UserSerializer
User=get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    event=EventListSerializer(read_only=True)

    class Meta:
        model=Registration
        fields=['id','user','event','qr_code','registration_code','checked_in','checked_in_at','registered_at']

        read_only_fields=['id','qr_code','registration_code','registered_at']