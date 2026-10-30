# INF601 - Advanced Programming in Python
# Gage Giffin
# Mini Project 6

from django.shortcuts import render


def home(request):
    return render(request, "campaigns/home.html")
