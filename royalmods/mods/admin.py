from django.contrib import admin
from .models import Game, Category, Mod, ModImage


class ModImageInline(admin.TabularInline):
    model = ModImage
    extra = 1
    max_num = 6


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Mod)
class ModAdmin(admin.ModelAdmin):
    list_display = ['name', 'game', 'main_author', 'status', 'views_count', 'downloads_count', 'created_at']
    list_filter = ['status', 'game', 'categories', 'created_at']
    search_fields = ['name', 'description', 'main_author__username']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['categories', 'other_authors', 'required_mods']
    inlines = [ModImageInline]
    
    actions = ['approve_mods', 'reject_mods']
    
    def approve_mods(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} mods approved successfully.')
    approve_mods.short_description = 'Approve selected mods'
    
    def reject_mods(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} mods rejected.')
    reject_mods.short_description = 'Reject selected mods'