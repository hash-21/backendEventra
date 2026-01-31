from rest_framework import serializers

from api.serializers import UserSerializer
from  .models import Session

class SessionSerializer(serializers.ModelSerializer):
    speaker=UserSerializer(read_only=True)
    speaker_id=serializers.IntegerField(write_only=True,required=False,allow_null=True)
    duration_minutes=serializers.ReadOnlyField()

    class Meta:
        model = Session
        fields=['id','event','title','description','speaker','speaker_id','speaker_name','speaker_bio','start_time','end_time','duration_minutes','room','track', 'topics', 'max_attendees',
            'created_at', 'updated_at']
        
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        if 'start_time' in attrs and 'end_time' in attrs:
            if attrs['start_time'] >= attrs['end_time']:
                raise serializers.ValidationError({
                    'end_time': 'End time must be after start time'
                })
        return attrs


class SessionListSerializer(serializers.ModelSerializer):
    speaker_name_display=serializers.SerializerMethodField()
    duration_minutes=serializers.ReadOnlyField()

    class Meta:
        model = Session
        fields=['id','title','speaker_name_display','start_time','end_time','duration_minutes','room','track']

    def get_speaker_name_display(self,obj):
        if obj.speaker:
            return obj.speaker.full_name
        return obj.speaker_name or 'TBA'


class SessionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields=['event','title','description','speaker','speaker_name','speaker_bio','start_time','end_time','room','track', 'topics', 'max_attendees']

    def validate(self, attrs):
        if 'start_time' in attrs and 'end_time' in attrs:
            if attrs['start_time'] >= attrs['end_time']:
                raise serializers.ValidationError({
                    'end_time': 'End time must be after start time'
                })
        if 'event' in attrs and 'start_time' in attrs and 'end_time' in attrs and 'room' in attrs:
            event=attrs['event']
            start=attrs['start_time']   
            end=attrs['end_time']  
            room=attrs['room']

            existing_sessions=Session.objects.filter(
                event=event,
                room=room,
            )

            if self.instance:
                existing_sessions = existing_sessions.exclude(id=self.instance.id)

            
            for session in existing_sessions:
                if start<session.end_time and end>session.start_time:
                    raise serializers.ValidationError({
                        'room': f'Time conflict with "{session.title}" in {room}'
                    })
        return attrs

               
               