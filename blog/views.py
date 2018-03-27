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

    def get_context_data(self, **kwargs):
        '''在视图函数中，将模板变量传递给模板使用render函数和context参数传递一个字典实现，
        但是在类视图中，传递模板变量是通过get_context_data获得的,所以通过复写的方法添加
        自定义的变量'''

        #首先获得父类生成的传递给模板的字典
        context = super().get_context_data(**kwargs)

        #父类生成的字典中已有 paginator,page_obj,is_paginated 这三个模板变量
        #paginator 是 Paginator 的一个实例
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        #调用自己写的paginator_data 方法获取显示分页导航条需要的数据
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        #将分页导航条的模板变量更新到context中，注意pagination_data方法返回的也是一个字典
        context.update(pagination_data)

        #将更新后的context返回，用于ListView使用这个字典中的模板变量去渲染模板
        #context中已经有了分页导航条需要的数据
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            #如果没有分页，无需导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}
        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第一页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第一页的
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号
        # 同理
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是[1,2,3,4]
        page_range = paginator.page_range

        if page_number == 1:
            # 只有一页的时候，那么当前页左边不需要数据，因此left=[]
            # 此时只需要获取分页后面的页码即可
            # 比如分页页码列表是[1,2,3,4] 那么获取 [2,3]即可
            # 这里是获取了页码后面两个连续页码，可以更改这个数字
            right = page_range[page_number:page_number + 2]

            # 如果最后变得页码号比最后一页的页码号减去1还小
            # 说明最右边的页码号和最后一页的页码号之间还有其他页码，因此需要显示省略号，通过 right_has_more 来标志
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一个页码号小，则表示连续页码号不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过last来标志
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果当前页码号等于最后一个页码号，那么当前页码右边就不需要数据，因此 right=[]
            # 此时只需要获取分页前面的连续页码即可
            # 比如分页页码列表是[1,2,3,4], 那么获取的就是[2,3]
            # 这里是获取了页码前面两个连续页码，可以更改这个数字
            left = page_range[(page_number-3) if (page_number-3) > 0 else 0 : page_number - 1]

            # 如果最左边的页码号比第2页页码号还大,
            # 说明最左边的页码号和第1页页码号之间可以使用省略号，
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第一页的页码号大，说明当前页左边的省略号中没有第一页，
            # 所以需要显示第一页的页码号，通过first标志
            if left[0] > 1:
                last = True
        else:
            # 用户请求的中间页码，需要获取左右两边的连续页码，
            # 当前只获取了前后两个页码，可以更改数字获取更多或更少
            left = page_range[(page_number - 3) if (page_range - 3) > 0 else 0 : page_number - 1]
            right = page_range[page_number : page_number + 2]

            # 是否需要显示后的省略号和最后页码号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示前的省略号和第一页码号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last
        }

        return data

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