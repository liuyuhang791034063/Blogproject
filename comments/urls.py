#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:grey_boy 
@file: urls.py 
@time: 2018/03/{DAY} 
"""
from django.conf.urls import url

from . import views

app_name = 'comments'
urlpatterns = [
    url(r'^comment/post/(?<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
]