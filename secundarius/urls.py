"""secundarius URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from deliveries.views import (stop_view, route_view, stale_token_view, 
    upload_view, upload_success_view)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', upload_view, name='upload'),
    path('<token_value>', route_view, name='route_view'),
    path('<token_value>/<stop_num>', stop_view, name='stop_view'),
    path('stale-token/', stale_token_view, name='stale_token'),
    path('upload-success/', upload_success_view, name='upload_success'),
]
