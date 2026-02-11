from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from django.contrib.auth.mixins import (
    LoginRequiredMixin, #We will use mixins as .login_required can't be used in class based views!!
    UserPassesTestMixin,
)

# Create your views here.

def home(request):
    context = {
        'posts':Post.objects.all()
    }

    return render(request, 'blog/home.html', context)

class PostListView(ListView): #Using class based views instead of fnx based views.
    model = Post
    template_name = 'blog/home.html' #Convention-1 : <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post #Create a new html page using Convention-1 which it will then use the template directly

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form): # A fnx to let the user(which is currently signed in) be the author of the post.
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form): # A fnx to let the user(which is currently signed in) be the author of the post.
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self): # To prevent any user to update other users post!!
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post 
    success_url = '/'
    def test_func(self): # To prevent any user to update other users post!!
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request,'blog/about.html', {'title':'About'})

 
