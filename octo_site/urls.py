
from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    #home and setup
    path('', views.index, name='index'),
    path('signout', views.signout, name='signout'),
    path('log_in/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    #settings
    path('add_room/', views.add_room, name='add_room'),
    path('add_sensor/', views.add_sensor, name='add_sensor'),
    path('add_branch/', views.add_branch, name='add_branch'),

    path('admin/', admin.site.urls),
]
