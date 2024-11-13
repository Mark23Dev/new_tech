from django.contrib import admin
from .models import Institution, Scholarship

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_partner', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('is_partner',)

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution', 'amount', 'application_deadline', 'is_active')
    search_fields = ('title', 'institution__name')
    list_filter = ('is_active', 'institution')
