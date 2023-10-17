from django.contrib import admin
from core.models import User, Post, Media

admin.site.register(User)

class MediaInline(admin.TabularInline):
    model = Media

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
    list_display = ('creater', 'caption', 'created_at')