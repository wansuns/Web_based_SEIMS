"""Web_based_SEIMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from app01 import views

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls, name="admin"),
    path('stu_list/', views.stu_list, name="slist"),
    path('stu_add/', views.stu_add, name="sadd"),
    path('stu_mod/<int:sid>', views.stu_mod, name="smod"),
    path('stu_del/<int:sid>', views.stu_del, name="sdel"),
    path('stu_search/', views.stu_search, name="search"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="reg"),
    path('image/code/', views.image_code, name="valid"),
    path('detect_face/', views.detect_face, name='model'),
    path('course/', views.course, name='course'),

]
from django.conf import settings
from django.conf.urls.static import static


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
print('urls.py:', static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))