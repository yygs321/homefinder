from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostDetailView, PostCreateView

urlpatterns = [
    path('community/', views.index, name='index'),
    #path('community/board/', views.board_list_view, name='board_list'),  # 게시판 목록 추가
    #path('community/board/<int:board_id>/', views.detail, name='board_detail'),  # 게시글 상세 보기
    #path('community/board/create/', views.create_board_view, name='board_create'),  # 게시글 작성
    path('sign-up/', views.sign_up_view , name='sign_up'),
    path('sign-in/', views.sign_in_view, name='sign_in'),
    path('gangnam/', views.gangnam_view, name='gangnam'),
    path('seocho/', views.seocho_view, name='seocho'),
    path('songpa/', views.songpa_view, name='songpa'),
    path('post_<int:board_id>/', PostDetailView.as_view(), name='post-detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('logout/', views.logout_view, name='logout'),
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
from django.urls import path
from . import views

