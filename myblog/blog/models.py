from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# 定义类别数据库表
class Category(models.Model):
	name = models.CharField(max_length=100)


# 定义标签数据库表
class Tag(models.Model):
	name = models.CharField(max_length=100)


# 定义文章数据库表
class Post(models.Model):
	# 文章标题
	title = models.CharField(max_length=70)
	# 文章正文
	body = models.TextField()
	# 文章创建时间
	created_time = models.DateTimeField()
	# 文章修改时间
	modified_time = models.DateTimeField()
	# 文章摘要（可有可无）
	excerpt = models.CharField(max_length=200, blank=True)
	# 文章所属类别
	category = models.ForeignKey(Category)
	# 文章所属标签
	tags = models.ManyToManyField(Tag, blank=True)
	# django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
	author = models.ForeignKey(User)


	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})