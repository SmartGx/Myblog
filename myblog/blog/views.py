from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm
from django.views.generic import ListView
import markdown

# 起始页
# def index(request):
# 	post_list = Post.objects.all()
# 	return render(request, 'blog/index.html', context={'post_list': post_list})
# 将index视图函数修改为类视图
class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'


# 文章详情页
def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.increase_views()
	post.body = markdown.markdown(post.body,
								  extensions=[
									  'markdown.extensions.extra',
									  'markdown.extensions.codehilite',
									  'markdown.extensions.toc',
								  ])
	form = CommentForm()
	# 获取这篇post下的全部评论
	commit_list = post.comment_set.all()

	context = {'post': post,
			   'form': form,
			   'comment_list': commit_list}
	return render(request, 'blog/detail.html', context=context)


# 归档页
# def archives(request, year, month):
# 	post_list = Post.objects.filter(created_time__year=year,
# 									created_time__month=month).order_by('-created_time')
# 	return render(request, "blog/index.html", context={"post_list": post_list})
class ArchivesView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
									created_time__month=self.kwargs.get('month')).order_by('-created_time')

# 分类页面
# def category(request, pk):
# 	cate = get_object_or_404(Category, pk=pk)
# 	post_list = Post.objects.filter(category=cate).order_by('-created_time')
# 	return render(request, 'blog/index.html', context={'post_list': post_list})
class CategoryView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	# 重写父类的get_queryset方法，该方法默认获取指定模型的全部列表数据
	def get_queryset(self):
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category=cate)