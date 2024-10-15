from django.urls import path
from . import views

urlpatterns = [
    path('gangnam/', views.gangnam_view, name='gangnam'),
    path('seocho/', views.seocho_view, name='seocho'),
    path('songpa/', views.songpa_view, name='songpa'),
]