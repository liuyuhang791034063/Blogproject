from ..models import Post, Category
from django import template

register = template.Library()

@register.simple_tag()
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag()
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag()
def get_categories():
    list = Post.objects.all()
    dict = {}
    for i in list:
        if i.category in dict:
            dict[i.category] +=1
        else:
            dict[i.category] = 1
    return dict

