from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    # post views
    path('login/', auth_views.LoginView.as_view(template_name='my_registration/login.html'), name='login'),
    #Si lo dejo como registration al menos asi como esta me manda es al admin
    path('logout/', auth_views.LogoutView.as_view(template_name='my_registration/logged_out.html'), name='logout'),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='my_registration/password_change_form.html'),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='my_registration/password_change_done.html'),name='password_change_done'),
    path('password_reset',auth_views.PasswordResetView.as_view(template_name='my_registration/password_reset_form.html'),name='password_reset'),
    path('password_reset/done',auth_views.PasswordResetDoneView.as_view(template_name='my_registration/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='my_registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done',auth_views.PasswordResetCompleteView.as_view(template_name='my_registration/password_reset_complete.html'),name='password_reset_complete'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('edit/', views.edit, name='edit'),
    path('', views.dashboard, name='dashboard'),
    
]