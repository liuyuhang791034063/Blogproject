#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:grey_boy 
@file: forms.py 
@time: 2018/03/{DAY} 
"""
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import  Post

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']

