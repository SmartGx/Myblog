from django.db import models


# 定义存储评论信息的数据库表
class Comment(models.Model):
	# 名字
	name = models.CharField(max_length=100)
	# Email地址
	email = models.EmailField(max_length=255)
	# 个人网站地址（选填）
	url = models.URLField(blank=True)
	# 评论文本内容
	text = models.TextField()
	# 评论创建时间
	created_time = models.DateTimeField(auto_now_add=True)

	# 对应的文章
	post = models.ForeignKey('blog.Post')

	def __str__(self):
		return self.text[:20]
