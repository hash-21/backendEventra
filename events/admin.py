from django.contrib import admin
from .models import Event
# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=['title','organizer','date','start_time','city','category','total_registrations','capacity']
    list_filter=['category','date','city']
    search_fields=['title','description','city']
    readonly_fields=['created_at','updated_at','total_registrations']
    date_hierarchy='date'

    fieldsets=(
        (
            'Basic Information',{
                'fields':('title','description','banner_image','organizer')
            }
        ),
        ('Date & Time', {
            'fields': ('date', 'start_time', 'end_time')
        }),
        ('Location', {
            'fields': ('venue_name', 'location', 'city', 'country')
        }),
        ('Details', {
            'fields': ('category', 'tags', 'capacity')
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at', 'total_registrations'),
            'classes': ('collapse',)
        }),
    )
