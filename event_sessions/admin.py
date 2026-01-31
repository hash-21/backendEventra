from django.contrib import admin
from .models import Session
# Register your models here.
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'speaker', 'start_time', 'end_time', 'room', 'track']
    list_filter=['event','track','room']
    search_fields=['title','description','speaker__email','speaker_name']
    readonly_fields=['created_at','updated_at','duration_minutes']

    fieldsets=(
        (
            'Session Info',{
                'fields':('event','title','description')
            }
        ),
         ('Speaker', {
            'fields': ('speaker', 'speaker_name', 'speaker_bio')
        }),
        ('Time', {
            'fields': ('start_time', 'end_time', 'duration_minutes')
        }),
        ('Location', {
            'fields': ('room', 'track')
        }),
        ('Details', {
            'fields': ('topics', 'max_attendees')
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),

    )

