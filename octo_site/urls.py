
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
    path('room/', views.page_room, name='page_room'),
    path('sensor/', views.page_sensor, name='page_sensor'),
    path('branch/', views.page_branch, name='page_branch'),

    path('admin/', admin.site.urls),
]
