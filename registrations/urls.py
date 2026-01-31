from django.urls import path, include
from . import views

urlpatterns=[
    path('my-registrations/',views.my_registrations,name='my_registrations'),
    path('check-in/',views.check_in,name='check_in'),
]