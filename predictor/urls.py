from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict-price/', views.predict_price, name='predict_price'),
    path('patterns/', views.patterns, name='patterns'),
]
