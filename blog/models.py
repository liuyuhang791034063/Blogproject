from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

@python_2_unicode_compatible#用于兼容python2
class Category(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name
@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length = 70)

    body = models.TextField()

    #这两个分别是创建时间和最后一次修改的时间,所以用DateTimeField类型
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length = 200, blank = True)
    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/1.10/topics/db/models/#relationships
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    tags = models.ManyToManyField(Tag, blank = True)
    #文章作者，User是从django.contrib.auth.models 导入
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return self.title
    #自定义get_absolute_url方法
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})#reverse函数逆向处理url，匹配相应的url值并且拿回来

    