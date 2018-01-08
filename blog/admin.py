from django.contrib import admin
from .models import Post, Profile, Comment

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'time')
	list_filter = ('title', 'author', 'time')
	search_fields = ('title', 'content')

class CommentAdmin(admin.ModelAdmin):
	list_display = ('parent_post', 'short_content', 'author', 'time')
	list_filter = ('parent_post', 'author', 'time')
	search_fields = ('parent_post__title', 'content', 'author__username')

admin.site.site_header = 'Administration'
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)
