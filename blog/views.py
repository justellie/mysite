from django.shortcuts import render, get_object_or_404
from django.core.paginator import  Paginator, EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Post, Comment
from .forms import EmailPostForm,CommentForm,SearchForm
from django.db.models import Count

class PostList(ListView):
    queryset = Post.published.all()#obtiene todos los post publicados
    context_object_name = 'posts'
    template_name='blog/post/list.html'
    paginate_by=3


    
class TagList(ListView):
    queryset = Post.published.all()#obtiene todos los post publicados
    context_object_name = 'posts'
    template_name='blog/post/list.html'
    paginate_by=3
    def get_queryset(self):
         queryset = Post.published.all()
         return queryset.filter(tags__name__in=[self.kwargs['tag_slug']])
    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context.update({
            'tag': self.kwargs['tag_slug']
        })
        return context
    

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    
    #Lista de comentaros activos para este post 
    comments=post.comments.filter(active=True)
    new_comment=None

    if request.method=='POST':
        #Un nuevo comentario fue posteado
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            #Crear el objecto comentario pero no salvarlo en base de datos 
            new_comment=comment_form.save(commit=False)
            #le asignamos el post actual 
            new_comment.post=post
            #guardamos el comentario en la base de datos
            new_comment.save()
    else:
        comment_form=CommentForm()
    
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]    
    ctx={'post':post,'new_comment':new_comment,'comment_form':comment_form,'comments':comments,'similar_posts': similar_posts}
    return render(request,'blog/post/detail.html',ctx)

def post_share(request, post_id):
    #Obtener por el ID
    post= get_object_or_404(Post,id=post_id,status='published')
    sent=False
    if request.method=='POST':
        #La data fue enviada
        form=EmailPostForm(request.POST)
        if form.is_valid():
            #data esta valida 
            cd=form.cleaned_data
            #mandados el email

            '''
            Since you have to include a link to the post in the email, you retrieve the absolute
                path of the post using its get_absolute_url() method. You use this path as an
                input for request.build_absolute_uri()
            '''
            post_url=request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'elioruiz.en@gmail.com',[cd['to']])
            sent = True
    else: # la data no fue enviada
        form=EmailPostForm()
    ctx={'post':post,'form':form,'sent':sent}
    return render(request,'blog/post/share.html',ctx)    

def post_search(request):

    form=SearchForm()
    query=None
    results=[]
    if 'query' in request.GET:
            form=SearchForm(request.GET)
            if form.is_valid():
                query= form.cleaned_data['query']
                search_vector=SearchVector('title','body')
                search_query=SearchQuery(query)
                results=Post.published.annotate(
                    search=SearchVector('title','body'),
                    rank=SearchRank(search_vector,search_query)
                ).filter(search=search_query).order_by('-rank')
    ctx={'form':form,'query':query,'results':results}
    return render(request,'blog/post/search.html',ctx)