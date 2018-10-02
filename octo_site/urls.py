
from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    #home and setup
    path('', views.index, name='index'),
    path('control_panel/', views.control_panel, name='control_panel'),
    path('signout', views.signout, name='signout'),
    path('log_in/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    #settings
    path('sensor/', views.page_sensor, name='page_sensor'),
    path('venue/', views.page_venue, name='page_venue'),

    path('admin/', admin.site.urls),
]
