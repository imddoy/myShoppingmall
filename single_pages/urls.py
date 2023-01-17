from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing),
    path('brand_story/',views.brand_story),
    path('mypage/', views.mypage),
]