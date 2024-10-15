from django.db import models

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
