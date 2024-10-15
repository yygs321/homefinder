from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.index, name='index'),  # 메인 페이지
]