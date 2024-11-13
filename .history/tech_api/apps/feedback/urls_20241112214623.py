# apps/feedback/urls.py
from django.urls import path
from .views import SubmitFeedbackView, ListFeedbackView, RetrieveFeedbackView, UpdateFeedbackView, DeleteFeedbackView

urlpatterns = [
    path('submit/', SubmitFeedbackView.as_view(), name='submit-feedback'),
    path('list/', ListFeedbackView.as_view(), name='list-feedback'),
    path('<int:pk>/', RetrieveFeedbackView.as_view(), name='retrieve-feedback'),
    path('<int:pk>/update/', UpdateFeedbackView.as_view(), name='update-feedback'),
    path('<int:pk>/delete/', DeleteFeedbackView.as_view(), name='delete-feedback'),
]
