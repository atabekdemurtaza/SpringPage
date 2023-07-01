from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','slug','author','publish','status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title']
    prepopulated_fields = {
        'slug': ('title',)
    }
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','post','created','active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name']

admin.site.register(Comment, CommentAdmin)

