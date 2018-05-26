# 存放和RSS订阅相关的代码,生成XML文档内容
from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
	# 显示在聚合阅读器上的标题
	title = 'Django 博客'

	# 通过聚合阅读器跳转到网站的地址
	link = '/'

	description = "Django 博客测试文章"

	# 需要显示的内容条目
	def items(self):
		return Post.objects.all()

	# 聚合阅读器中显示的内容条目的标题
	def item_title(self, item):
		return '[%s] %s' % (item.category.name, item.title)

	# 聚合器中显示的内容条目的表述
	def item_description(self, item):
		return item.body