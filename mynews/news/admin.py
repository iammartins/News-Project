from django.contrib import admin
from .models import Post, Category
#from ckeditor.widgets import CKEditorWidget
from django_ckeditor_5.widgets import CKEditor5Widget
from django.db import models

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'approved')
    list_filter = ('approved',)
    actions = ['approve_selected_posts', 'reject_selected_posts']

    def approve_selected_posts(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, f"{queryset.count()} posts successfully approved.")
    approve_selected_posts.short_description = "Approve selected posts"

    def reject_selected_posts(self, request, queryset):
        queryset.update(approved=False)
        self.message_user(request, f"{queryset.count()} posts successfully rejected.")
    reject_selected_posts.short_description = "Reject selected posts"

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            obj.approved = True
        super().save_model(request, obj, form, change)

    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget()},
    }


admin.site.register(Post, PostAdmin)
admin.site.register(Category)


