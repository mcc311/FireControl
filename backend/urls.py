"""backend URL Configuration

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
from django.urls import path, include, register_converter
from rest_framework.routers import DefaultRouter
from Vessel.views import MissileViewSet, VesselViewSet
from . import converters
from .views import index, redirect, testPOST, get_map
register_converter(converters.FloatUrlParameterConverter, 'float')
router = DefaultRouter()
router.register(r'missile', MissileViewSet)
router.register(r'vessel', VesselViewSet)
urlpatterns = [
    path('index/', index),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/test', testPOST),
    path('map', get_map),
    path(r'map/<int:z>/<float:x>/<float:y>',  redirect),

]
