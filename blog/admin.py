from django.contrib import admin
from .models import Post, Comment
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    '''
        You have
        told Django to prepopulate the slug field with the input of the title field using
        the prepopulated_fields attribute.
    '''
    prepopulated_fields = {'slug': ('title',)}
    '''
    Also, the author field is now displayed with a lookup widget that can scale much
    better than a drop-down select input when you have thousands of users. This is
    achieved with the raw_id_fields attribute and it looks like this:
    '''
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter=('active','created','updated')
    search_fields=('name','email','body')    

