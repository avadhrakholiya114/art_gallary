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
     path('art/<str:category>/', views.art, name='art'),
     path('art/', views.art, name='art_all'),
     path('artwork_detail/<int:id>', views.artwork_detail,name='artwork_detail'),
     path('cart/<int:id>', views.cart,name='cart'),
      path('show_cart/', views.show_cart, name="show_cart"),
      path('removecart/', views.removecart, name="removecart"),
      path('add_address/', views.add_address, name="add_address"),
      path('show_address/', views.show_address, name="show_address"),
      path('delete_address/<int:id>', views.delete_address, name="delete_address"),
      
      path('checkout/', views.checkout, name="checkout"),
      path('paymentdone/', views.paymentdone, name="paymentdone"),
      path('order/', views.order, name="order"),
      path('receiveorder/', views.receiveorder, name="receiveorder"),
      path('update_order_status/', views.update_order_status, name="update_order_status"),
]   