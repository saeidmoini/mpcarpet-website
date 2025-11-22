from django.contrib import admin
from .models import ContactMessage, Product


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'processed', 'created_at')
    list_filter = ('processed', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('message', 'ip_address', 'user_agent', 'created_at')
    actions = ('mark_processed', 'mark_unprocessed')

    def mark_processed(self, request, queryset):
        updated = queryset.update(processed=True)
        self.message_user(request, f"Marked {updated} message(s) as processed.")
    # Django <3.2 compatibility: set the action description via attribute
    mark_processed.short_description = 'Mark selected messages as processed'

    def mark_unprocessed(self, request, queryset):
        updated = queryset.update(processed=False)
        self.message_user(request, f"Marked {updated} message(s) as unprocessed.")
    mark_unprocessed.short_description = 'Mark selected messages as unprocessed'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'visible', 'featured', 'order', 'created_at')
    list_editable = ('visible', 'featured', 'order')
    search_fields = ('title', 'slug', 'specs')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('visible', 'featured')
