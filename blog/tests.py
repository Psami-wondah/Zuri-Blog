from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from .models import Post, Comments
from .views import signup
from django import forms

from django.contrib.auth.forms import UserCreationForm




# Create your tests here.
class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='secret',
        )

        self.post = Post.objects.create(
            title='A good title',
            body='Nice body',
            author=self.user
        )

        self.comment = Comments.objects.create(
            body='Nice Comment',
            author=self.user,
            post= self.post,



        )

    def test_string_representation(self):
        post = Post(title='A simple title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'A good title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Nice body')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A good title')
        self.assertTemplateUsed(response, 'home.html')


    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/100000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A good title')
        self.assertContains(response, 'Nice Comment')
        self.assertTemplateUsed(response, 'post_detail.html')
        form = response.context.get('form')
        self.assertIsInstance(form, forms.ModelForm)

    def test_comment_list_view(self):
        response = self.client.get('/post/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice Comment')


    def test_comment_content(self):
        self.assertEqual(f'{self.comment.post}', 'A good title')
        self.assertEqual(f'{self.comment.author}', 'testuser')
        self.assertEqual(f'{self.comment.body}', 'Nice Comment')


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('register')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/register/')
        self.assertEquals(view.func, signup)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)

class SignInTests(TestCase):
    pass

class ResetPassWordTests(TestCase):
    pass
class LogOutTests(TestCase):
    pass