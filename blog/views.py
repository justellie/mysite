from django.shortcuts import render, get_object_or_404
from django.core.paginator import  Paginator, EmptyPage,PageNotAnInteger
from .models import Post

def post_list(request):
    posts=Post.published.all()#obtiene todos los post publicados
    paginator=Paginator(posts,3)#tres post por pagina
    page=request.GET.get('page')#obtiene el numero de la pagina

    try:
        posts=paginator.page(page)#obtengo los tres post de dicha pagina
    except PageNotAnInteger:
        #Si la page no es un entero entonces muestra la primera pagina 
        posts=paginator.page(1)
    except EmptyPage:
        #Si page esta fuera de rango devuelve la ultima pagina
        posts=paginator.page(paginator.num_pages)

    '''
    Since the Page object you are passing to the template is called posts, you include
    the pagination template in the post list template, passing the parameters to render
    it correctly.
    '''

    ctx={'posts':posts,'page':page}
    return render(request,'blog/post/list.html',ctx)

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    ctx={'post':post}
    return render(request,'blog/post/detail.html',ctx)