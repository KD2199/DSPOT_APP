from django.urls import path
from .views import initiate_payment, callback
from . import views

urlpatterns = [
    path('pay/<int:Did>', views.initiate_payment, name='pay'),
    path('callback/', views.callback, name='callback'),
]