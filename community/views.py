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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 자치구 이름을 추가로 전달
        context['district_name'] = "강남구"  # 강남구 예시