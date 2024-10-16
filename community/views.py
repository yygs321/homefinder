from django.shortcuts import render, redirect

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse
from .models import *

# 회원가입 기능
def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        nickname = request.POST.get('nickname', None)

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
                new_user.nickname = nickname
                new_user.save()
                return redirect('/sign-up')
            
# 로그인 기능
def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        me = UserModel.objects.get(username=username)
        if me.password == password:
            request.session['user'] = me.username
            return HttpResponse(f'로그인 성공! {me.username}님 환영합니다!')
        else:
            return redirect('/sign-in')
    
    elif request.method == 'GET':                    
        return render(request, 'user/signin.html')

# 게시판
def detail(request, board_id):
    board = BoardModel.objects.get(id=board_id)
    context = {'board': board}
    return render(request, 'community/detail.html', context)

def create_board_view(request):
    if request.method == 'GET':
        return render(request, 'community/create_board.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        contents = request.POST.get('contents')
        region_id = request.POST.get('region_id')
        username = request.user  # 현재 로그인한 사용자

        new_board = BoardModel(title=title, contents=contents, region_id=region_id, username=username)
        new_board.save()
        return redirect('index')


def index(request):
    return render(request, 'community/index.html')  # index.html 템플릿을 렌더링

def board_list_view(request):
    boards = BoardModel.objects.all()  # 모든 게시글 조회
    context = {'boards': boards}
    return render(request, 'community/board_list.html', context)  # board_list.html 템플릿 렌더링
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Post

def gangnam_view(request):
    return render(request, 'gangnam.html')

def seocho_view(request):
    return render(request, 'seocho.html')

def songpa_view(request):
    return render(request, 'songpa.html')

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        board_id = self.kwargs.get('board_id')
        return self.model.objects.get(board_id=board_id)  # post_id를 사용하여 객체 가져오기