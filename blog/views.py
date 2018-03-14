#coding=utf-8

from django.shortcuts import render,get_object_or_404
from .models import Post


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk = pk)#get_object_or_404 函数的作用是如果pk值存在的话返回正确的post，否则返回404错误
    return render(request, 'blog/detail.html', context={'post':post})