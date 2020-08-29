from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User #modelo de usuarios que ya trae django
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                self).get_queryset()\
                    .filter(status='published') 

# Create your models here.
class Post(models.Model):
    LENGTH=250
    STATUS_CHOICES=(
        ('draft','Draft'),
        ('published','Published'),
    )    
    title= models.CharField(max_length=LENGTH)
    '''
    This is a field intended to be used in URLs. A slug is a short label
    that contains only letters, numbers, underscores, or hyphens. You will use
    the slug field to build beautiful, SEO-friendly URLs for your blog posts.
    '''
    slug=models.SlugField(max_length=LENGTH, unique_for_date='publish')
    '''
    You specify the name of the reverse relationship,
    from User to Post, with the related_name attribute. This will allow you to
    access related objects easily.
    '''
    author=models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    body=models.TextField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    publish=models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                        self.publish.month,
                        self.publish.day, self.slug])
