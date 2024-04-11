from django.urls import path
from . import views

urlpatterns = [

     path('', views.home,name='home'),
      path('about/', views.about,name='about'),
      path('register/', views.register,name='register'),
       path('login_view/', views.login_view,name='login'),
       path('logout/', views.logout_view,name='logout'),
]