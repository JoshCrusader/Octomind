
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
    path('list_user/', views.list_user, name='list_user'),
    #game dets
    path('game_logs/', views.game_logs, name='game_logs'),
    path('game_logs/game/<int:game_id>/', views.game_logs_detail, name='game_logs_detail'),
    path('game_logs/analysis/<slug:game_ids>/', views.analyze_game_logs, name='analyze_game_logs'),
    #settings
    path('sensor/', views.page_sensor, name='page_sensor'),
    path('venue/', views.page_venue, name='page_venue'),
    path('sensor_data/<int:game_id>/',views.sensor_data, name='sensor_data'),
    path('all_sensor_data/',views.all_sensor_data, name='all_sensor_data'),

    path('api/get_log_distribution/<slug:game_ids>/', views.get_log_distribution, name='get_log_distribution'),
    path('api/get_log_summary/<slug:game_ids>/', views.get_log_summary, name='get_log_summary'),

    path('api/game_summary/<int:game_id>/', views.game_summary, name='game_summary'),
    path('api/game_tally/<int:game_id>/', views.game_tally, name='game_tally'),
    #ajax functions
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
    path('api/get_clues_by_game/<int:game_id>/', views.get_clues_by_game, name = 'get_clues_by_game'),
    path('api/get_players_data/', views.get_players_data, name = 'get_players_data'),
    path('api/get_market/', views.get_market, name = 'get_market'),
    path('api/get_room_market/', views.get_room_market, name = 'get_room_market'),
    path('api/get_exception_data/', views.get_exception_data, name = 'get_exception_data'),
    path('api/get_clue_data/<int:game_id>/', views.get_clue_data, name='get_clue_data'),
    path('api/select_sensor_data/<slug:game_ids>/', views.select_sensor_data, name='select_sensor_data'),
    path('api/get_all_time_data/<int:room_id>/', views.get_all_time_data, name='get_all_time_data'),
    path('api/get_all_time_data_sensor/<int:sensor_id>/', views.get_all_time_data_sensor, name='get_all_time_data_sensor'),
    #reports
    path('reports/room_analysis', views.room_analysis, name='room_analysis'),
    path('reports/room_details_analysis', views.room_details_analysis, name='room_details_analysis'),
    path('reports/sensor_analysis', views.sensor_analysis,name='sensor_analysis'),
    path('reports/trend_analysis', views.trend_analysis, name='trend_analysis'),
    path('reports/player_analysis_report', views.player_analysis_report, name = 'player_analysis_report'),
    path('reports/market_analysis', views.market_analysis, name = 'market_analysis'),
    path('reports/market_report', views.market_report, name='market_report'), ## test url only
    path('reports/map_market_report', views.map_market_report, name='map_market_report'), ## test url only
    path('reports/exception_report', views.exception_report, name='exception_report'),
    path('reports/exception_report_details', views.exception_report_details, name='exception_report_details'),
    #testinging
    path('sandbox_analysis/<int:room_id>/', views.sandbox_analysis, name='sandbox_analysis'),
    path('sample_marker', views.sample_marker, name='sample_marker'),

    #test_urls
    path('data_vis/<int:room_id>/', views.data_vis, name='data_vis'),
    path('data_vis_v2/<int:game_id>/', views.data_vis_v2, name='data_vis_v2'),
    path('live_monitor/<int:game_id>/', views.live_monitoring, name='live_monitor'),
    path('log_distribution/<slug:game_ids>/', views.log_distribution, name='log_distribution'),
    path('log_summary/<slug:game_ids>/', views.log_summary, name='log_summary'),
    path('log_percentage_complete/<slug:game_ids>/', views.log_percentage_complete, name='log_percentage_complete'),
    ##
    #handlers
    path('error404/', views.handler404, name='error404'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)