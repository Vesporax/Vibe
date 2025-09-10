from django.contrib import admin
from .models import SiteConfiguration, PageTemplate


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'allow_registrations', 'maintenance_mode', 'updated_at']
    fieldsets = [
        ('General Settings', {
            'fields': ('site_name', 'site_description', 'featured_mods_count')
        }),
        ('Access Control', {
            'fields': ('allow_registrations', 'maintenance_mode', 'maintenance_message')
        }),
    ]
    
    def has_add_permission(self, request):
        """Only allow one site configuration"""
        return not SiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of site configuration"""
        return False


@admin.register(PageTemplate)
class PageTemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    
    actions = ['activate_pages', 'deactivate_pages']
    
    def activate_pages(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} pages activated successfully.')
    activate_pages.short_description = 'Activate selected pages'
    
    def deactivate_pages(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} pages deactivated.')
    deactivate_pages.short_description = 'Deactivate selected pages'