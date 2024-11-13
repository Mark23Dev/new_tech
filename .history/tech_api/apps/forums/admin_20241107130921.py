from django.contrib import admin
from .models import ForumPost, ForumComment

class CommentInline(admin.TabularInline):
    model = ForumComment
    extra = 1

class PostInline(admin.TabularInline):
    model = ForumPost
    extra = 1

@admin.register(ForumPost)  # Registering ForumPost with ForumAdmin
class ForumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    inlines = [PostInline]

@admin.register(ForumPost)  # Registering Post with PostAdmin
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'forum', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('forum', 'author')
    inlines = [CommentInline]

@admin.register(ForumComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('post', 'author')

