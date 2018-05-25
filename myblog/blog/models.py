from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown

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
	# views字段用于记录阅读量(非负值)
	views = models.PositiveIntegerField(default=0)

	# 获取文章对应的URL
	def get_absolute_url(self):
		return reverse('blog:detail', kwargs={'pk': self.pk})

	# 每次访问文章的detail页面， 阅读量+1
	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

	# 重写模型的save方法,将正文字段摘取N个字符保存到摘要中
	def save(self, *args, **kwargs):
		if not self.excerpt:
			# 首先实例化一个Markdown对象，用于渲染body的文本
			md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
			# 先将markdown文本渲染成HTML文本
			# strip_tags去掉HTML文本的全部HTML标签
			# 从文本摘取前54个字符付给excerpt
			self.excerpt = strip_tags(md.convert(self.body))[:54]
			
		# 调用父类的save方法将数据保存到数据库中
		super(Post, self).save(*args, **kwargs)

	# 定义文章排序方式
	class Meta:
		ordering = ['-created_time']
