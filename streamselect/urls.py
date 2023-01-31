from django.contrib import admin

from django.urls import path
from django.contrib.auth import views as auth_views

import streamselect.views as stream_views

urlpatterns = [
    path('', stream_views.home, name='home'),
    path('login/', stream_views.user_login, name='login'),
    path('register/', stream_views.register, name='register'),
    path('profile/', stream_views.profile, name='profile'),
    #path('forgot_pwd/', views.forgot_pwd, name='forgot_pwd'),
    path('password_change', stream_views.password_change, name='password_change'),
    path('password_reset', stream_views.password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>', stream_views.password_reset_confirm, name='password_reset_confirm'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
