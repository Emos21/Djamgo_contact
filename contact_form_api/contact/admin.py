from django.contrib import admin
from .models import Contact, HireRequest

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
    )
@admin.register(HireRequest)
class HireRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'get_service_display', 'created_at', 'updated_at')
    list_filter = ('service_needed', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')  # Add this line

    # Remove created_at/updated_at from fieldsets
    fieldsets = (
        ('Client Information', {
            'fields': ('email',)
        }),
        ('Service Details', {
            'fields': ('service_needed',)
        }),
    )

    def get_service_display(self, obj):
        return obj.get_service_needed_display()
    get_service_display.short_description = 'Service Requested'