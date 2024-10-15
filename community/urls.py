from django.urls import path
from . import views
from .views import PostDetailView

urlpatterns = [
    path('gangnam/', views.gangnam_view, name='gangnam'),
    path('seocho/', views.seocho_view, name='seocho'),
    path('songpa/', views.songpa_view, name='songpa'),
    path('post_<int:board_id>/', PostDetailView.as_view(), name='post-detail'),
]