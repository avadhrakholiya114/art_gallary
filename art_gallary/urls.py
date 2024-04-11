from django.urls import path
from . import views

urlpatterns = [

     path('', views.home,name='home'),
      path('about/', views.about,name='about'),
      path('register/', views.register,name='register'),
       path('login_view/', views.login_view,name='login'),
       path('logout/', views.logout_view,name='logout'),
       path('profile/', views.profile,name='profile'),
       path('sell_art/', views.sell_art,name='sell_art'),
     #   path('artwork_detail/<int:id>', views.artwork_detail,name='artwork_detail'),
     path('art/', views.art,name='art'),
     # path('artwork_detail/<int:id>', views.artwork_detail,name='artwork_detail'),
     path('artwork_detail/', views.artwork_detail,name='artwork_detail')
     
]