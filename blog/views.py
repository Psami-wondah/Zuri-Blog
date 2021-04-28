from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Post
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, NewCommentForm, PostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import database


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'


# class BlogCreateView(CreateView): same as the Detail view
#     model = Post
#     template_name = 'post_new.html'
#     fields = ['title', 'author', 'body']


class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']


class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')

# class BlogDetailView(DetailView): So here I couldn't use a class based view here so I switched to a function view below
#     model = Post
#     template_name = 'post_detail.html'





def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            database.create(username, raw_password, email)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm
    return render(request, 'register.html', {'form': form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)
                messages.info(request, f'You are now logged in as {username}')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    return render(request=request, template_name='login.html', context={'login_form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have sucessfully logged out.")
    return redirect("login")



def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post = post
            data.author = user
            data.save()
            return redirect('post_detail', pk = pk)
    else:
        form = NewCommentForm()
    return render(request, 'post_detail.html', {'post':post, 'form':form})


def post_form(request):
    user = request.user
    if request.method == 'POST':
        form =PostForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.author = user
            data.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'post_new.html', {'form':form})



