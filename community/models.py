from django.db import models

from django.utils import timezone
import datetime

# Create your models here.
from django.db import models


class UserModel(models.Model): # 사용자
    username = models.CharField(max_length=20,verbose_name='유저ID') # 유저ID
    nickname = models.CharField(max_length=20) # ID
    password = models.CharField(max_length=20) # 비밀번호
    created_date = models.DateTimeField('date published') # 생성일
    
class BoardModel(models.Model):
    board_id = models.CharField(max_length=20) # 게시판 ID 
    title = models.CharField(max_length=64,verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    username = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    region_id = models.CharField(max_length=20) # 지역 ID
    created_date = models.DateTimeField('date published') # 생성일

    def __str__(self):
        return self.username

# class Comment(models.Model): # 댓글
#     comment_id = models.CharField(max_length=20) # 댓글 ID
#     board_id = models.CharField(max_length=50) # 커뮤니티 ID
#     username = models.ForeignKey(User, on_delete=models.CASCADE) # 댓글 작성자 ID
#     content = models.CharField(max_length=50) # 댓글 내용
#     created_date = models.DateTimeField('date published') # 생성일
#     # votes = models.IntegerField(default=0)
#     #is_something = models.BooleanField(default=False)
#     #average_score = models.FloatField(default=0.0)

#     def __str__(self):
#         return f'{self.article_id}, 댓글작성자ID: {self.comment_id}, {self.created_date}'
class Post(models.Model):
    board_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE) 
    region_id = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title  # 게시물 제목을 반환

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
