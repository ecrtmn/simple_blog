from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Post, Tag
from .utils import ObjectDetailMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .forms import TagForm, PostForm, CreateUserForm


def posts_lists(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    return render(request, 'blog/index.html', context={'posts': posts})


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})


def custom_registration(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Profile successfuly created for ' + user + '!')
            return redirect('custom_login')
    return render(request, 'register.html', context={'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('posts_list_url')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'login.html')


def custom_logout(request):
    logout(request)
    return redirect('custom_login')

class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete.html'
    redirect_url = 'tags_lists_url'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update.html'
    raise_exception = True


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model = TagForm
    path = 'blog/tag_create.html'
    raise_exception = True


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model = PostForm
    path = 'blog/post_create.html'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    path = 'blog/tag_detail.html'


class PostDetail(ObjectDetailMixin, View):
    model = Post
    path = 'blog/post_detail.html'
