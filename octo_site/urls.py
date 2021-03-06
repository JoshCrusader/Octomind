
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
    path('registration/', views.registration, name='registration'),
    #game dets
    path('game_logs/', views.game_logs, name='game_logs'),
    path('game_logs/game/<int:game_id>/', views.game_logs_detail, name='game_logs_detail'),
    path('game_logs/analysis/<slug:game_ids>/', views.analyze_game_logs, name='analyze_game_logs'),
    #settings
    path('sensor/', views.page_sensor, name='page_sensor'),
    path('venue/', views.page_venue, name='page_venue'),
    path('sensor_data/<int:game_id>/',views.sensor_data, name='sensor_data'),
    path('all_sensor_data/',views.all_sensor_data, name='all_sensor_data'),
        #settings api
    path('api/get_log_distribution/<slug:game_ids>/', views.get_log_distribution, name='get_log_distribution'),
    path('api/get_log_summary/<slug:game_ids>/', views.get_log_summary, name='get_log_summary'),

    path('api/game_summary/<int:game_id>/', views.game_summary, name='game_summary'),
    path('api/game_tally/<int:game_id>/', views.game_tally, name='game_tally'),

    #view room screen
    path('tv_monitor/', views.tv_monitor, name='tv_monitor'),
    path('tv_monitor/<int:game_id>/', views.tv_monitor, name='tv_monitor_screen'),
    #ajax functions
    path('api/update_plot/', views.update_plot, name='update_plot'),
    path('api/get_sensor_by_game/<int:game_id>/', views.get_sensor_by_game, name='get_sensor_by_game'),

    path('api/get_game_durations/<slug:game_ids>/', views.get_game_durations, name='get_game_durations'),
    path('api/get_game_duration/<int:game_id>/', views.get_game_duration, name='get_game_duration'),
    path('api/get_sensor_by_room_id/<int:room_id>/', views.get_sensors_by_room_id, name='get_sensors_by_room_id'),
    path('api/get_clues_list_by_room/<int:room_id>/', views.get_clues_list_by_room, name='get_clues_list_by_room'),
    path('api/get_room_by_room_id/<int:room_id>/', views.get_room_by_room_id, name='get_room_by_room_id'),
    path('api/game_cur_logs/<int:game_id>/', views.game_cur_logs, name='game_cur_logs'),
    path('api/get_cur_games/', views.get_cur_games, name = 'get_cur_games'),
    path('api/get_player_list/', views.get_player_list, name = 'get_player_list'),
    path('api/start_game/', views.start_game, name = 'start_game'),
    path('api/end_game/', views.end_game, name = 'end_game'),
    path('api/confirm_end_game/', views.confirm_end_game, name = 'confirm_end_game'),
    path('api/add_clue/', views.add_clue, name = 'add_clue'),
    path('api/get_clues_by_game/<int:game_id>/', views.get_clues_by_game, name = 'get_clues_by_game'),
    path('api/get_players_data/', views.get_players_data, name = 'get_players_data'),
    path('api/get_market/', views.get_market, name = 'get_market'),
    path('api/get_room_market/', views.get_room_market, name = 'get_room_market'),
    path('api/get_exception_data/', views.get_exception_data, name = 'get_exception_data'),
    path('api/get_clue_data/<int:game_id>/', views.get_clue_data, name='get_clue_data'),
    path('api/get_clues_data/<slug:game_ids>/', views.get_clues_data, name='get_clue_data'),

    path('api/select_sensor_data/<slug:game_ids>/', views.select_sensor_data, name='select_sensor_data'),
    path('api/get_all_time_data/<int:room_id>/', views.get_all_time_data, name='get_all_time_data'),
    path('api/check_notifs/', views.check_notif, name='check_notif'),
    path('api/open_notifs/', views.open_notif, name='open_notif'),
    path('api/get_cohort_analysis/<slug:game_ids>/', views.cohort_analysis, name='cohort_analysis'),

    path('api/get_cur_phase/<int:game_id>/', views.get_cur_phase, name='get_cur_phase'),

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
    path('data_vis/', views.data_vis, name='data_vis'),
    path('data_vis_v2/<int:game_id>/', views.data_vis_v2, name='data_vis_v2'),
    path('live_monitor/<int:game_id>/', views.live_monitoring, name='live_monitor'),
    path('log_distribution/<slug:game_ids>/', views.log_distribution, name='log_distribution'),
    path('log_summary/<slug:game_ids>/', views.log_summary, name='log_summary'),
    path('log_percentage_complete/<slug:game_ids>/', views.log_percentage_complete, name='log_percentage_complete'),
    path('log_summary/<slug:game_ids>/', views.log_summary, name='log_summary'),

    ##
    #handlers
    path('error404/', views.handler404, name='error404'),
    path('admin/', admin.site.urls),

    #Sscripts
    path('scripts/script_helper', views.script_helper_v, name = "script_helper"),
    path('scripts/add_mins/', views.add_mins, name = "add_mins"),
    path('scripts/set_end_min/', views.set_end_time, name = "set_end_time"),
    path('scripts/add_logs/', views.add_script_logs, name = "add_logs"),
    path('scripts/add_clue/', views.add_script_clue, name = "add_clue"),
    #iot
    path('live_monitor_iot/', views.live_monitoring_iot, name='live_monitor_iot'),
    path('sensor_data_iot/<slug:timestart>',views.sensor_data_iot, name='sensor_data_iot'),

    #populate
    path('populateme/', views.popstart, name='populatestart'),
    path('populatehim/', views.pophim, name='populatehim'),
    path('populatehim/', views.pophim, name='populatehim'),
    path('randomfunc/', views.randomfunc, name='randomfunc'),


    #additional dashboard apis
    path('api/get_p_cities/', views.get_p_cities, name = 'get_p_cities'),
    path('api/get_locs_dashboard/', views.get_locs_dashboard, name = 'get_locs_dashboard'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)