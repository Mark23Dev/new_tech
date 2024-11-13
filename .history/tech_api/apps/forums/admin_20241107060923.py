from django.contrib import admin
from .models import Forum, Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class PostInline(admin.TabularInline):
    model = Post
    extra = 1

@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    inlines = [PostInline]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'forum', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('forum', 'author')
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('post', 'author')
