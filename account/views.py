
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm,UserEditForm, ProfileEditForm
from .models import Profile

# Create your views here.

def user_login(request):

    if request.method=='POST':
        
        form=LoginForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user= authenticate(request,username=cd['username'],password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse('Authenticated succesfully')
                else:
                    return HttpResponse('Diseabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form=LoginForm()
    ctx={'form':form}
    return render(request,'account/login.html',{'form':form})


class RegisterView(CreateView):
    form_class=UserRegistrationForm
    success_url='account/register_done.html'
    template_name='account/register.html'
    def form_valid(self, form):
        self.info_sended = True
        # Instead of return this HttpResponseRedirect, return an 
        #  new rendered page
        super(RegisterView, self).form_valid(form)
        Profile.objects.create(user= self.object)
        return render(self.request, self.success_url,
                      self.get_context_data(form=form))


@login_required 
def dashboard(request):
    ctx={'section':'dashboard'}
    return render(request,'account/dashboard.html',ctx)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile update successfully')
            HttpResponseRedirect(reverse('edit'))
        else:
            messages.error(request,'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})