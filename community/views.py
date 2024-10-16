from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from .models import *
# 회원가입 기능
def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)

        if password != password2:
            return render(request, 'user/signup.html')
        else:
            exist_user = UserModel.objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html')
            else:
                new_user = UserModel()
                new_user.username = username
                new_user.password = password
                new_user.nickname = username
                new_user.created_date = datetime.datetime.now()
                new_user.save()
                return redirect(request, '/gangnam')
            
# 로그인 기능
def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        
        try:
            me = UserModel.objects.get(username=username)
            if me.password == password:
                request.session['user'] = me.username
                return render(request, 'gangnam.html', {'username': me.username})  # 로그인 성공 시 gangnam.html 렌더링
            else:
                return redirect('/community/sign-in')
        except UserModel.DoesNotExist:
            return redirect('/community/sign-in')  # 유저가 존재하지 않을 때도 다시 로그인 페이지로 리다이렉트

    elif request.method == 'GET':                    
        return render(request, 'user/signin.html')

def logout_view(request):
    if 'user' in request.session:
        del request.session['user']  # 세션에서 'user'를 삭제하여 로그아웃 처리
    return redirect('/community/gangnam')  # 로그아웃 후 로그인 페이지로 리다이렉트


# 게시판
# 게시글 상세 보기
def detail(request, board_id):
    board = BoardModel.objects.get(id=board_id)
    context = {'board': board}
    return render(request, 'community/detail.html', context)

# 메인페이지
def index(request):
    return render(request, 'community/index.html')  # index.html 템플릿을 렌더링

# 게시글 목록 보기
def board_list_view(request):
    boards = BoardModel.objects.all()  # 모든 게시글 조회
    context = {'boards': boards}
    return render(request, 'community/board_list.html', context)  # board_list.html 템플릿 렌더링

def gangnam_view(request):
    posts = Post.objects.filter(region_id='강남')
    return render(request, 'gangnam.html', {'posts': posts})

def seocho_view(request):
    posts = Post.objects.filter(region_id='서초')
    return render(request, 'seocho.html', {'posts': posts})

def songpa_view(request):
    posts = Post.objects.filter(region_id='송파')
    return render(request, 'songpa.html', {'posts': posts})

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        board_id = self.kwargs.get('board_id')
        return self.model.objects.get(board_id=board_id)  # post_id를 사용하여 객체 가져오기

#@login_required  # 로그인한 사용자만 글 작성 가능
class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    context_object_name = 'post'
    fields = ['region_id', 'title', 'content']  # 폼에 포함될 필드들

    def form_valid(self, form):
        # 현재 로그인한 사용자 추가
        form.instance.user_id = self.request.user
        return super().form_valid(form)
    
    success_url = '/community/gangnam/'

