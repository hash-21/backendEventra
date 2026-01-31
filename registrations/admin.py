from django.contrib import admin
from .models import Registration
# Register your models here.
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display=['user','event','registration_code','checked_in','registered_at']
    list_filter=['checked_in','registered_at','event']
    search_fields=['user__email','event__title','registration_code']
    readonly_fields=['qr_code','registration_code','registered_at','checked_in_at']
    date_hierarchy='registered_at'


    fieldsets=(
        ('Registration Info',{
            'fields':('user','event','registration_code','registered_at')
        }),
        ('Qr Code',{
            'fields':('qr_code',)
        }),
        ('Check-in Info',{
            'fields':('checked_in','checked_in_at')
        })
    )
