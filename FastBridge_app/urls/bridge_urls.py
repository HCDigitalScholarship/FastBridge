from django.urls import path
from FastBridge_app.views.bridge.latin.latin_view import LatinView
from FastBridge_app.views.bridge.views import index

urlpatterns = [
    path('', index, name='index'),
    path('latin/', LatinView.as_view()),
    ]
