"""
Main view for The Bridge search request form
"""
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

