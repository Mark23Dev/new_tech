from django.contrib import admin
from .models import Feedback, Testimonial

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'approved')
    list_filter = ('approved',)
    search_fields = ('author__username', 'content')
    ordering = ('-created_at',)

# Register your models here
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
