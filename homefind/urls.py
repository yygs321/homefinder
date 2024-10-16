from django.urls import path, include

from . import views
from .views import *

urlpatterns = [
    path('index',views.index),
    path('map',views.map),
]
