"""
URL configuration for vulnwebapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('catalog/', include('catalog.urls')),
    path('profile/<slug:slug>/', include('catalog.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', views.custom_login, name='login'),
    path('nslookup/', views.using_cmd, name='dns'),
    path('photo/', views.cool_photo, name='photo'),
    path('', RedirectView.as_view(url='/accounts/login')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
