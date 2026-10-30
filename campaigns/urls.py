# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 6

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
]
