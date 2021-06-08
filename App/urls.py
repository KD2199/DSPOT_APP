'''
  @author Karan Dave  
'''

from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='HomePage'),
    path('about/', views.about, name='About'),
    path('msg/', views.msg, name='msg'),
    path('blog/', views.blog, name='blog'),
    path('detail/', views.detail, name='detail'),
    path('send/', views.send, name='send'),
    path('requests/', views.requests, name='requests'),
    path('Accept/', views.Accept, name='Accept'),
    path('work/', views.work, name='work'),
    path('Followers/', views.Followers, name='Followers'),
    path('Following/', views.Following, name='Following'),
    path('remove/', views.remove, name='remove'),
    path('unfollow/', views.unfollow, name='unfollow'),
    path('cart/', views.cart, name='cart'),
    path('cartItem/', views.cartItem, name='cartItem'),
    path('Cremove/', views.Cremove, name='Cremove'),
    path('Save/', views.Save, name='Save'),
    path('usave/', views.usave, name='usave'),
    path('delete/', views.delete, name='delete'),
    path('LKS/', views.LKS, name='LKS'),
    path('Category/', views.Category, name='Category'),
    path('posts/', views.posts, name='posts'),
    path('feedback/', views.feedback, name='feedback'),
    path('chat/', views.chat, name='chat'),
    path('cleartalk/', views.cleartalk, name='cleartalk'),
    path('makepb/', views.makepb, name='makepb'),
    path('makepv/', views.makepv, name='makepv'),
    path('psdt/', views.psdt, name='psdt'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('mypurchased/', views.mypurchased, name='mypurchased'),
    path('order_history/', views.order_history, name='order_history'), 
    path('sorder/', views.sorder, name='sorder'),
    path('Testimonials/', views.Testimonials, name='Testimonials'),
    
]
