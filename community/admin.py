from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserModel)
admin.site.register(BoardModel)

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('board_id', 'user_id', 'region_id', 'title', 'created_date')
    search_fields = ('title', 'content')
