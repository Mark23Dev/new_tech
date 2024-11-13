from django.urls import path
from .views import EventListView, EventDetailView, EventRegisterView, UserParticipationView, EventCalendarView

urlpatterns = [
    path('all/', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('register/', EventRegisterView.as_view(), name='event-register'),
    path('calendar/', EventCalendarView.as_view(), name='event-calendar'),
    path('participation/', UserParticipationView.as_view(), name='user-participation'),
]
