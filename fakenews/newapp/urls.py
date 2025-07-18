from django.urls import path, include
from . import views

urlpatterns = [
    path('predict/', views.predict_news, name='predict_news'),
]
