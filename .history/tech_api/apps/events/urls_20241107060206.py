from django.urls import path
from .views import (
    EventListView,
    EventDetailView,
    RegisterEventView,
    UserEventHistoryView,
    EventActivityLogView,
)

urlpatterns = [
    path('all/', EventListView.as_view(), name='event-list'),
    path('<int:event_id>/', EventDetailView.as_view(), name='event-detail'),
    path('register/<int:event_id>/', RegisterEventView.as_view(), name='event-register'),
    path('participation/', UserEventHistoryView.as_view(), name='user-event-history'),
    path('<int:event_id>/logs/', EventActivityLogView.as_view(), name='event-activity-log'),
]
