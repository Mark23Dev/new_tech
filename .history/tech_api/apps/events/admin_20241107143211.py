from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'created_at')  # Customize fields for display
    search_fields = ('name', 'location')  # Fields to search by in the admin interface
    list_filter = ('date',)  # Fields to filter by in the admin sidebar
    ordering = ('-date',)  # Order events by date in descending order

# If you have additional models in events, you can register them similarly:
# admin.site.register(AnotherModel)
