from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comments
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm, NewCommentForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import database
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# Create your views here.


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'


# class CommentListView(ListView):
#     model = Comments
#     template_name = 'comment_list.html'


# class BlogCreateComment(CreateView):
#     model = Comments
#     template_name = 'new_comment.html'
#     fields = ['author', 'body']



# class BlogDetailView(DetailView):
#     model = Post
#     template_name = 'post_detail.html'


class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body']


class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']


class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('home')



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


# def password_reset_request(request):
#     if request.method == "POST":
#         password_reset_form = PasswordResetForm(request.POST)
#         if password_reset_form.is_valid():
#             data = password_reset_form.cleaned_data['email']
#             associated_users = User.objects.filter(Q(email=data))
#             if associated_users.exists():
#                 for user in associated_users:
#                     subject = "Password Reset Requested"
#                     email_template_name = "password/password_reset_subject.txt"
#                     c = {
#                         "email":user.email,
#                         'domain':'127.0.0.1:8000',
#                         'site_name': 'Website',
#                         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                         "user": user,
#                         'token': default_token_generator.make_token(user),
#                         'protocol': 'http',
#                     }
#                     email = render_to_string(email_template_name, c)
#                     try:
#                         send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
#                     except BadHeaderError:
#                         return HttpResponse('Invalid header found.')
#                     messages.success(request, 'A message with reset password instructions has been sent to your email.')
#                     return redirect("home")
#             messages.error(request, 'An invalid email has been entered.')
#     password_reset_form = PasswordResetForm()
#     return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

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





# @login_required
# def reply_topic(request, pk):
#     topic = get_object_or_404(Post, pk)
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.topic = topic
#             post.created_by = request.user
#             post.save()
#             return redirect('post_detail', pk=pk)
#     else:
#         form = PostForm()
#     return render(request, 'home.html', {'topic': topic, 'form': form})