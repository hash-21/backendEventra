from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display=['email','username','first_name','last_name','role','date_joined']
    list_filter=['role','is_staff','is_active']
    search_fields=['email','username','first_name','last_name']
    ordering=['-date_joined']

    fieldsets=BaseUserAdmin.fieldsets+(
        ('Profile Information',{
            'fields': ('profile_picture', 'bio', 'role', 'interests')
        }),
           ('Location', {
            'fields': ('city', 'country')
        }),
        ('Social Links', {
            'fields': ('linkedin_url',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name', 'role', 'interests', 'city', 'country')
        }),
    )

    
