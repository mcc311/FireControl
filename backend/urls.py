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
# from Battlefield.views import BattlefieldView
from . import converters
from .views import index, profile, login, table, handler404, VesselListView, VesselUpdateView, MissileUpdateView, MissileListView
from Battlefield.views import testPOST, get_result, get_map, get_policy_index_ver
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="FireControl API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="daniel2000890311.cs07@nycu.edu.tw"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
register_converter(converters.FloatUrlParameterConverter, 'float')
router = DefaultRouter()
router.register(r'missile', MissileViewSet)
router.register(r'vessel', VesselViewSet)
urlpatterns = [
    path('', index),
    path('index/', index),
    path('get_policy/', get_policy_index_ver),
    path('profile/', profile),
    path('login/', login),
    path('table/vessel', VesselListView.as_view(), name='vessel_table'),
    path('table/vessel/<int:pk>', VesselUpdateView.as_view(success_url="/table/vessel"), name='vessel_update_table'),
    path('table/missile', MissileListView.as_view(), name='missile_table'),
    path('table/missile/<int:pk>', MissileUpdateView.as_view(success_url="/table/missile"), name='missile_update_table'),
    path('404/', handler404),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/getPolicy', testPOST),
    path(r'map/', get_map),
    path(r'map/<int:bid>', get_result, name='get_result'),
    path('api/doc', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
