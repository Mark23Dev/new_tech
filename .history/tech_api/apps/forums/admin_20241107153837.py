from django.contrib import admin
from .models import ForumPost, ForumComment

class CommentInline(admin.TabularInline):
    model = ForumComment
    extra = 1

@admin.register(ForumPost)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    inlines = [CommentInline]  # Use CommentInline to show related comments

@admin.register(ForumComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at', 'updated_at')
    search_fields = ('content',)
    list_filter = ('post', 'author')
