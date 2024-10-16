from django.urls import path, include

from . import views
from .views import *

urlpatterns = [
    path('mapdata/', MapData.as_view()),
    path('scountbygu/', ForSaleCountByGu.as_view()),
    path('scountbytype/', ForSaleCountByType.as_view()),
    path('scountbycat/', ForSaleCountByCategory.as_view()),
    path('wclouddata/', WordCloudData.as_view()),
    path('heatdata/', HeatMapData.as_view()),

    path('index',views.index),
    path('map',views.map),
]
