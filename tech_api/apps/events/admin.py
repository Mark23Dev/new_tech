from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'location', 'created_at')  # Using correct field names
    search_fields = ('title', 'location')  # Searching by title and location
    list_filter = ('start_time',)  # Filtering by start_time
    ordering = ('-start_time',)  # Ordering by start_time in descending order
