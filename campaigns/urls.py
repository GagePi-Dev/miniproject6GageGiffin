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
]
