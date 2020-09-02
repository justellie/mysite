from django import template 
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown 
from ..models import Post

register=template.Library()

'''
Each module that contains template tags needs to define a variable called
register to be a valid tag library.
'''
@register.simple_tag
def total_posts():
    return Post.published.count()

'''
Using an inclusion tag, you can render
a template with context variables returned by your template tag.
'''
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
                total_comments=Count('comments')
            ).order_by('-total_comments')[:count]  

'''
You register template filters in the same way as template tags. To prevent a name
clash between your function name and the markdown module, you name your
function markdown_format and name the filter markdown for use in templates, such
as {{ variable|markdown }}.
'''
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))