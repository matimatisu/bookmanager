from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length = 200) #本のタイトル200文字までOK
    author = models.CharField(max_length = 100) #著者名
    published_date = models.DateField() #発売日
    is_read = models.BooleanField(default = False) #読んだかどうか
    read_date = models.DateField(null=True,blank=True) #読了日
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.title #管理画面でタイトルを表示できるようにする
# Create your models here.
