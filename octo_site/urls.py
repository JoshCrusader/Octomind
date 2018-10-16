
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    #home and setup
    path('', views.index, name='index'),
    path('control_panel/', views.control_panel, name='control_panel'),
    path('view_room/', views.view_room, name='view_room'),
    path('signout', views.signout, name='signout'),
    path('log_in/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    #settings
    path('sensor/', views.page_sensor, name='page_sensor'),
    path('venue/', views.page_venue, name='page_venue'),
    path('data_vis/<int:room_id>/',views.data_vis,name='data_vis'),
    path('sensor_data/<int:room_id>/',views.sensor_data, name='sensor_data'),
    #ajax functions
    path('api/upload_process/', views.upload_process,name='upload_process'),
    path('api/get_sensor_by_room_id/<int:room_id>/', views.get_sensors_by_room_id, name='get_sensors_by_room_id'),
    path('admin/', admin.site.urls),
    #reports
    path('reports/room_analysis', views.room_analysis, name='room_analysis'),
    path('reports/sensor_analysis', views.sensor_analysis,name='sensor_analysis'),
    path('reports/trend_analysis', views.trend_analysis, name='trend_analysis')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)