from django.urls import path
from .views import SubmitFeedbackView, AddTestimonialView, ListTestimonialsView

urlpatterns = [
    path('submit/', SubmitFeedbackView.as_view(), name='submit_feedback'),
    path('testimonials/add/', AddTestimonialView.as_view(), name='add_testimonial'),
    path('testimonials/list/', ListTestimonialsView.as_view(), name='list_testimonials'),
]
