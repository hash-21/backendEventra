from django.urls import path
from . import views

urlpatterns=[
    path('', views.get_all_events, name='get-all-events'),
    path('create/', views.create_event, name='create-event'),
    path('my-events/', views.get_my_events, name='my-events'),
    path('<int:pk>/', views.get_event_detail, name='event-detail'),
    path('<int:pk>/update/', views.update_event, name='update-event'),
    path('recommendations/',views.get_event_recommendations,name='event-recommendations'),
    path('<int:pk>/delete/', views.delete_event, name='delete-event'),
    path('<int:event_id>/register/', views.register_for_event, name='register-for-event'),
    path('<int:event_id>/unregister/', views.unregister_from_event, name='unregister-from-event'),
]