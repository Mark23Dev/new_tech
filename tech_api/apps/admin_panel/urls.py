# admin_panel/urls.py

from django.urls import path
from .views import UserActivityLogListView, UserActivityLogDetailView, UserActivityLogCreateView, UserActivityLogClearView

urlpatterns = [
    path('activity-logs/', UserActivityLogListView.as_view(), name='activity_log_list'),
    path('activity-logs/<int:log_id>/', UserActivityLogDetailView.as_view(), name='activity_log_detail'),
    path('activity-logs/create/', UserActivityLogCreateView.as_view(), name='activity_log_create'),
    path('activity-logs/clear/', UserActivityLogClearView.as_view(), name='activity_log_clear'),
]
