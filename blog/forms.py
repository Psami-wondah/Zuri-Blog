from django import forms
from .models import Post, Comments
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']

# class NewPostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'body']
