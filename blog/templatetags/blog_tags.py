from ..models import Post, Category, Tag
from django import template
from django.db.models.aggregates import Count

register = template.Library()

@register.simple_tag()
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]

@register.simple_tag()
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')

@register.simple_tag()
def get_categories():
    # list = Post.objects.all()
    # dict = {}
    # for i in list:
    #     if i.category in dict:
    #         dict[i.category] +=1
    #     else:
    #         dict[i.category] = 1
    # return dict
    # 记得导入count函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts = Count('post')).filter(num_posts__gt=0)

@register.simple_tag()
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)