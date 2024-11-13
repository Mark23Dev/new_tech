from django.urls import path
from apps.events.views import (
    EventListView, EventDetailView, RegisterEventView, UserEventHistoryView, 
    EventActivityLogView, CalendarView, EventAttendeeView, 
    EventViewSet, EventAttendeeViewSet, UserActivityLogViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'event-attendees', EventAttendeeViewSet)
router.register(r'user-activity-logs', UserActivityLogViewSet)

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/register/<int:event_id>/', RegisterEventView.as_view(), name='event-register'),
    path('user/events/', UserEventHistoryView.as_view(), name='user-event-history'),
    path('events/<int:event_id>/activity-log/', EventActivityLogView.as_view(), name='event-activity-log'),
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('event-attendees/', EventAttendeeView.as_view(), name='event-attendees'),
] + router.urls
