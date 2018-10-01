
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    #home and setup
    path('', views.index, name='index'),
    path('signout', views.signout, name='signout'),
    path('log_in/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    #settings
    path('sensor/', views.page_sensor, name='page_sensor'),
    path('venue/', views.page_venue, name='page_venue'),

    path('api/upload_process/', views.upload_process,name='upload_process'),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
