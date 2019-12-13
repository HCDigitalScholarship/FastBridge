from django.urls import path
from FastBridge_app.views.bridge.latin.latin_view import LatinView

urlpatterns = [
        path('', LatinView.as_view()),
    ]
