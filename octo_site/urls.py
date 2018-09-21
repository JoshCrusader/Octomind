
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signout', views.signout, name='signout'),
    path('log_in/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
]
