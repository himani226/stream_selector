from django.contrib import admin

from django.urls import path
from django.contrib.auth import views as auth_views

import streamselect.views as stream_views

urlpatterns = [
    path('', stream_views.index, name='index'),
    path('index/', stream_views.index, name='index'),
    path('home/', stream_views.home, name='home'),
    path('login/', stream_views.user_login, name='login'),
    path('register/', stream_views.register, name='register'),
    path('profile/', stream_views.profile, name='profile'),
    path('result/', stream_views.result, name='result'),
    path('section_first/', stream_views.section_first, name='section_first'),
    path('section_second/', stream_views.section_second, name='section_second'),
    path('section_three/', stream_views.section_three, name='section_three'),
    path('section_four/', stream_views.section_four, name='section_four'),
    path('section_five/', stream_views.section_five, name='section_five'),
    path('section_six/', stream_views.section_six, name='section_six'),
    path('section_seven/', stream_views.section_seven, name='section_seven'),
    path('section_eight/', stream_views.section_eight, name='section_eight'),
    path('section_nine/', stream_views.section_nine, name='section_nine'),
    path('section_ten/', stream_views.section_ten, name='section_ten'),
    path('disclaimer_stream/', stream_views.disclaimer_stream, name='disclaimer_stream'),
    path('disclaimer_career/', stream_views.disclaimer_career, name='disclaimer_career'),
    #path('generate_report/', stream_views.generate_report.as_view(), name='generate_report'),
    #path('generate_report/', stream_views.generate_report, name='generate_report'),
    path('checkout/', stream_views.checkout, name='checkout'),
    path('checkout/payment_handler/', stream_views.payment_handler, name='payment_handler'),
    path('password_change', stream_views.password_change, name='password_change'),
    path('password_reset', stream_views.password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>', stream_views.password_reset_confirm, name='password_reset_confirm'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
