from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .forms import ImageCreateForm
from .models import Image
# Create your views here.
@login_required
def image_create(request):
    if request.method=='POST':
        #form is sent
        form=ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            new_item=form.save(commit=False)
            #assing current user to the data
            new_item.user=request.user
            new_item.save()
            messages.success(request,'Image added successfully')

            #redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form=ImageCreateForm(data=request.GET)
    ctx={'section':'images','form':form}
    return render(request,'images/image/create.html',ctx)

def image_detail(request,id,slug):
    image=get_object_or_404(Image, id=id,slug=slug)
    ctx={'section':'images','image':image}
    return render(request,'images/image/detail.html',ctx)


'''
The require_POST decorator
returns an HttpResponseNotAllowed object (status code 405) if the HTTP request
is not done via POST. This way, you only allow POST requests for this view
'''
@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id=request.POST.get('id')
    action=request.POST.get('action')
    if image_id and action:
        try:
            image=Image.objects.get(id=image_id)
            if action=='like':
                image.user_like.add(request.user)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except :
            pass
    return JsonResponse({'status':'error'})

@login_required
def image_list(request):
    images=Image.objects.all()
    paginator=Paginator(images,8)
    page=request.GET.get('page')
    try:
        images=paginator.page(page)
    except PageNotAnInteger:
        #Si la pagina no es un entero entrego la primera
        images=paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            #Si el request es un ajax y la pagina esta fuera de rango 
            #retorna vacio
            return HttpResponse('')
        #Si la pagina esta fuera de rango entrega la ultima pagina de resultados
        images=paginator.page(paginator.num_pages)
    if request.is_ajax():
        ctx={'section':'images','images':images}
        return render(request,'images/image/list_ajax.html',ctx)
    ctx={'section':'images','images':images}
    return render(request,'images/image/list.html',ctx)
    