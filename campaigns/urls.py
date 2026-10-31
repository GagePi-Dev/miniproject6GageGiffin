# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 6

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("campaigns/", views.campaign_list, name="campaign_list"),
    path("campaigns/new/", views.campaign_create, name="campaign_create"),
    path("campaigns/join/", views.campaign_join, name="campaign_join"),
    path("campaigns/<int:pk>/", views.campaign_detail, name="campaign_detail"),
    path("campaigns/<int:pk>/edit/", views.campaign_edit, name="campaign_edit"),
    path("campaigns/<int:pk>/delete/", views.campaign_delete, name="campaign_delete"),
    path("campaigns/<int:pk>/sessions/", views.session_list, name="session_list"),
    path("campaigns/<int:pk>/sessions/new/", views.session_create, name="session_create"),
    path("campaigns/<int:pk>/sessions/<int:sid>/", views.session_detail, name="session_detail"),
    path("campaigns/<int:pk>/sessions/<int:sid>/edit/", views.session_edit, name="session_edit"),
    path("campaigns/<int:pk>/sessions/<int:sid>/delete/", views.session_delete, name="session_delete"),
    path("campaigns/<int:pk>/npcs/", views.npc_list, name="npc_list"),
    path("campaigns/<int:pk>/npcs/new/", views.npc_create, name="npc_create"),
    path("campaigns/<int:pk>/npcs/<int:nid>/edit/", views.npc_edit, name="npc_edit"),
    path("campaigns/<int:pk>/npcs/<int:nid>/delete/", views.npc_delete, name="npc_delete"),
]
