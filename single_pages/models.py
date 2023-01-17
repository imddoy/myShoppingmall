from django.db import models
from shop.models import Category
from django.contrib.auth.models import User

# Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True) #유일한값 가져야 함
#     slug = models.SlugField(max_length=200,unique=True, allow_unicode=True) #읽을 수 있는 text로 url #한글 사용 가능
#
#     def __str__(self):
#         return self.name
#     def get_absolute_url(self):
#         return f'/shop/category/{self.slug}/'
#     class Meta: #복수형 지정
#         verbose_name_plural='Categories'