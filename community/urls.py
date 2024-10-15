from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('community/', views.index, name='index'),
    path('community/board/', views.board_list_view, name='board_list'),  # 게시판 목록 추가
    path('community/board/<int:board_id>/', views.detail, name='board_detail'),  # 게시글 상세 보기
    path('community/board/create/', views.create_board_view, name='board_create'),  # 게시글 작성
    path('sign-up/', views.sign_up_view , name='sign_up'),
    path('sign-in/', views.sign_in_view, name='sign_in'),
]


# from django.urls import path, include
# from .views import *

# urlpatterns = [
#     path('mapdata/', MapData.as_view()),
#     path('scountbygu/', ForSaleCountByGu.as_view()),
#     path('scountbytype/', ForSaleCountbyType.as_view()),
#     path('scountbycat/', ForSaleCountbyCategory.as_view()),
#     path('wclouddata/', WordCloudData.as_view()),
#     path('heatdata/', HeatMapData.as_view()),
# ]