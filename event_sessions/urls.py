from django.urls import path
from . import views 

urlpatterns=[
   path('events/<int:event_id>/sessions/', views.get_event_sessions, name='event-sessions'),
    path('create/', views.create_session, name='create-session'),
    path('<int:pk>/', views.get_session_detail, name='session-detail'),
    path('<int:pk>/update/', views.update_session, name='update-session'),
    path('<int:pk>/delete/', views.delete_session, name='delete-session'),
]