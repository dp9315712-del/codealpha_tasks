from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='event-list'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),
    path('events/<int:pk>/register/', views.register_event, name='register-event'),
    path('my-registrations/', views.my_registrations, name='my-registrations'),
    path('registrations/<int:pk>/cancel/', views.cancel_registration, name='cancel-registration'),
]
