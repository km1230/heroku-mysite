from django.contrib import admin
from .models import Post, Profile, Comment

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'create_time', 'edit_time')
	list_filter = ('title', 'author', 'create_time', 'edit_time')
	search_fields = ('title', 'content')

class CommentAdmin(admin.ModelAdmin):
	list_display = ('parent_post', 'short_content', 'author', 'create_time', 'edit_time')
	list_filter = ('parent_post', 'author', 'create_time', 'edit_time')
	search_fields = ('parent_post__title', 'content', 'author__username')

admin.site.site_header = 'Administration'
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile)
