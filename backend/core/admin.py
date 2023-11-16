from django.contrib import admin
from core.models import User, Post, Media, Comment

admin.site.register(User)
admin.site.register(Media)


class MediaInline(admin.TabularInline):
    model = Media

class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [MediaInline, CommentInline]
    list_display = ('creater', 'caption', 'created_at')