"""
Created by : Karan Dave
"""

from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('outh/', include('allauth.urls')),
    path('',views.home,name='index'),
    path('home/',include('App.urls')),
    path('Account/', include('Account.urls')),
    path('payment/', include('Payment.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

