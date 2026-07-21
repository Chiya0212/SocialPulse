from django.contrib import admin
from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'privacy', 'is_flagged', 'is_hidden', 'created_at')
    list_filter = ('privacy', 'is_flagged', 'is_hidden')
    search_fields = ('content', 'author__username')
    actions = ['hide_posts', 'unhide_posts']

    def hide_posts(self, request, queryset):
        queryset.update(is_hidden=True)
    def unhide_posts(self, request, queryset):
        queryset.update(is_hidden=False)


admin.site.register(Comment)
admin.site.register(Like)
