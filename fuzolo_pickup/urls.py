"""
URL configuration for fuzolo_pickup project.

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
from os import name
from django.contrib import admin
from django.urls import path, include

# for images 
from django.conf import settings
from django.conf.urls.static import static

from .views import view_pickup, create_pickup, details_pickup

urlpatterns = [
    path('admin/', admin.site.urls),

    #users views
    path('accounts/', include('users.urls')),

    #fuzolo_pickup views
    path('view_pickup/', view_pickup, name = 'view-pickup'),
    path('creat_pickup/', create_pickup, name = 'create-pickup'),
    path('details_pickup/<game_id>/', details_pickup, name = 'details-pickup'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
