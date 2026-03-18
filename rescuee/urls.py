from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ----------- PUBLIC -----------
    path('', views.index),
    path('about/', views.about),
    path('marine_rescue/', views.marine_rescue),
    path('weather_alert/', views.weather_alert),
    path('contact/', views.contact),

    # ----------- AUTH -----------
    path('login/', views.login_view),
    path('register/', views.fisherman_register),
    path('rescue_register/', views.rescue_register),

    # ----------- ADMIN -----------
    path('admin_home/', views.admin_home),
    path('admin_add_weather_alert/', views.admin_add_weather_alert),
    path('admin_view_fishermen/', views.admin_view_fishermen),
    path('admin_view_sos/', views.admin_view_sos),
    path('admin_view_rescue/', views.admin_view_sos_rescue),
    path('admin_approve_rescue/', views.admin_approve_rescue),
    path('admin_add_weather_alert/', views.admin_add_weather_alert),
    path('admin_edit_weather_alert/', views.admin_edit_weather_alert),
    path('admin_delete_weather_alert/', views.admin_delete_weather_alert),
    path('admin_view_weather/', views.admin_view_weather),
    path('admin_add_port/', views.admin_add_port),
    path('admin_view_ports/', views.admin_view_port),
    path('admin_edit_port/', views.admin_edit_port),
    path('admin_delete_port/', views.admin_delete_port),
    path('admin_view_rescue_team/', views.admin_view_rescue),
    path('admin_approve_rescue/', views.admin_approve_rescue),
    path('admin_block_rescue/', views.admin_block_rescue),
    path('admin_reject_rescue/',views. admin_reject_rescue),



    # ----------- FISHERMAN -----------
    path('fisherman_home/', views.fisherman_home),
    path('fisherman_view_weather/', views.fisherman_view_weather),
    path('send_sos/', views.send_sos),
    path('fisherman_sos_history/', views.fisherman_sos_history),

    # ----------- RESCUE TEAM -----------
    path('rescue_home/', views.rescue_home),
    path('rescue_view_sos/', views.rescue_view_sos),
    path('rescue_take_action/', views.rescue_take_action),
    path('rescue_history/', views.rescue_history),
    path('rescue_history_detail/', views.rescue_history_detail),

]
