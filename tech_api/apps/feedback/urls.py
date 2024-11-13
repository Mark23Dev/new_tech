from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.feedback.views import SubmitFeedbackView, ListFeedbackView, RetrieveFeedbackView, UpdateFeedbackView, DeleteFeedbackView, TestimonialViewSet

router = DefaultRouter()
router.register(r'testimonials', TestimonialViewSet)

urlpatterns = [
    path('feedback/submit/', SubmitFeedbackView.as_view(), name='submit-feedback'),
    path('feedback/', ListFeedbackView.as_view(), name='list-feedback'),
    path('feedback/<int:pk>/', RetrieveFeedbackView.as_view(), name='retrieve-feedback'),
    path('feedback/<int:pk>/update/', UpdateFeedbackView.as_view(), name='update-feedback'),
    path('feedback/<int:pk>/delete/', DeleteFeedbackView.as_view(), name='delete-feedback'),
    path('', include(router.urls)),
]
