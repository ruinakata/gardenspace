"""gardenspaceproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
    https://github.com/alanjds/drf-nested-routers
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers 
from gardenspace import views

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'plants', views.PlantViewSet)
router.register(r'my_plants', views.MyPlantViewSet)
router.register(r'locations', views.LocationViewSet)
# router.register(r'location_my_plants', views.LocationMyPlantViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', include(router.urls)),
    path('location_my_plants/', views.LocationMyPlantView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
