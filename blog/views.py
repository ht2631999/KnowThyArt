from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from users.models import User

# Create your views here.

#make login_required out of comment while deploying the project






#@login_required	
def home(request):

	context={
		'posts': Post.objects.all(),
		'title': 'BLOG'

	}
	return render(request, 'blog/home.html',context)


class PostListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

	#The browser looks for url pattern <app>/<modeL>_<viewtype>.html, when we use class type view 
	# instead of function type views(as def home or about)

class UserPostListView(LoginRequiredMixin, ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username= self.kwargs.get('username'))
		return Post.objects.filter(author= user).order_by('-date_posted')

	
		
class PostDetailView(LoginRequiredMixin, DetailView):
	model = Post
	#<app>/<modeL>_<viewtype>.html
	#template browser will look for blog/post_detail.html

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = [ 'title', 'content', 'activity', 'register_url']
	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	#<app>/<modeL>_<viewtype>.html
	#template browser will look for blog/post_detail.html

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = [ 'title', 'content', 'activity' , 'register_url']
	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	#test_func is used by UserPassesTestMixin to determine whether the user trying to 
	#access the update facility for the current post (self.object) is the author of it or not
	#as only author must be allowed to update it
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	#test_func is used by UserPassesTestMixin to determine whether the user trying to 
	#access the delete facility for the current post (self.object) is the author of it or not
	#as only author must be allowed to delete it
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False
	#<app>/<modeL>_<viewtype>.html
	#template browser will look for blog/post_detail.html

#@login_required
def about(request):
	context={
		'title': 'About Title'
	}
	return render(request,'blog/about.html', context)