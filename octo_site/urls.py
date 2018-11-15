
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    #home and setup
    path('', views.index, name='index'),
    path('control_panel/', views.control_panel, name='control_panel'),
    path('view_room/<int:game_id>', views.view_room, name='view_room'),
    path('signout', views.signout, name='signout'),
    path('log_in/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    #game dets
    path('game_logs/', views.game_logs, name='game_logs'),
    path('game_logs/game/<int:game_id>/', views.game_logs_detail, name='game_logs_detail'),
    #settings
    path('sensor/', views.page_sensor, name='page_sensor'),
    path('venue/', views.page_venue, name='page_venue'),
    path('sensor_data/<int:game_id>/',views.sensor_data, name='sensor_data'),
    path('all_sensor_data/',views.all_sensor_data, name='all_sensor_data'),
    #test_urls
    path('data_vis/<int:room_id>/', views.data_vis, name='data_vis'),
    path('data_vis_v2/<int:game_id>/', views.data_vis_v2, name='data_vis_v2'),
    path('live_monitor/<int:game_id>/', views.live_monitoring, name='live_monitor'),
    path('api/game_summary/<int:game_id>/', views.game_summary, name='game_summary'),
    path('api/game_tally/<int:game_id>/', views.game_tally, name='game_tally'),
    #ajax functions
    path('api/upload_process/', views.upload_process,name='upload_process'),
    path('api/update_plot/', views.update_plot, name='update_plot'),
    path('api/get_sensor_by_game/<int:game_id>/', views.get_sensor_by_game, name='get_sensor_by_game'),
    path('api/get_sensor_by_room_id/<int:room_id>/', views.get_sensors_by_room_id, name='get_sensors_by_room_id'),
    path('api/get_room_by_room_id/<int:room_id>/', views.get_room_by_room_id, name='get_room_by_room_id'),
    path('api/game_cur_logs/<int:game_id>/', views.game_cur_logs, name='game_cur_logs'),
    path('api/get_cur_games/', views.get_cur_games, name = 'get_cur_games'),
    path('api/get_player_list/', views.get_player_list, name = 'get_player_list'),
    path('api/start_game/', views.start_game, name = 'start_game'),
    path('api/end_game/', views.end_game, name = 'end_game'),
    path('api/add_clue/', views.add_clue, name = 'add_clue'),
    path('api/get_players_data/', views.get_players_data, name = 'get_players_data'),
    path('api/get_market/', views.get_market, name = 'get_market'),
    path('admin/', admin.site.urls),
    #reports
    path('reports/room_analysis', views.room_analysis, name='room_analysis'),
    path('reports/room_details_analysis', views.room_details_analysis, name='room_details_analysis'),
    path('reports/sensor_analysis', views.sensor_analysis,name='sensor_analysis'),
    path('reports/trend_analysis', views.trend_analysis, name='trend_analysis'),
    path('reports/market_report', views.market_report, name='market_report'),

    #testinging
    path('sandbox_analysis/<int:room_id>/', views.sandbox_analysis, name='sandbox_analysis'),
    path('sample_marker', views.sample_marker, name='sample_marker')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)