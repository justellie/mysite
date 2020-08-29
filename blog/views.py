from django.shortcuts import render, get_object_or_404
from django.core.paginator import  Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .models import Post


class PostList(ListView):
    queryset = Post.published.all()#obtiene todos los post publicados
    context_object_name = 'posts'
    template_name='blog/post/list.html'
    paginate_by=3

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    ctx={'post':post}
    return render(request,'blog/post/detail.html',ctx)