#coding=utf-8

import markdown
from django.shortcuts import render,get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView


# def index(request):
#     post_list = Post.objects.all().order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list':post_list,})

# def detail(request, pk):
#     post = get_object_or_404(Post, pk = pk)#get_object_or_404 函数的作用是如果pk值存在的话返回正确的post，否则返回404错误
#     post.increase_views()
#
#     post.body = markdown.markdown(post.body,['extra','codehilite','toc',])
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     context = {'post':post,
#                 'form':form,
#                 'comment_list':comment_list,
#                 }
#     return render(request, 'blog/detail.html', context=context)

# def archives(request, year, month):
#     post_list = Post.objects.filter(created_time__year = year,
#                                     created_time__month = month,
#                                     ).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list':post_list})
#
# def category(request, pk):
#     cate = get_object_or_404(Category, pk = pk)
#     post_list = Post.objects.filter(category=cate).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list':post_list})

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year =year,
                                                               created_time__month =month)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 文章加1
        # self.object 的值就是被访问的文章post
        self.object.increase_views()

        #视图必须返回一个HttpResponse对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, ['extra', 'codehilite', 'toc', ])
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form' : form,
            'comment_list' : comment_list,
        })
        return context