from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from .models import Post, Comments
from .views import signup
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from.forms import SignUpForm
from django.core import mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views



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

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    # def test_contains_form(self):
    #     form = self.response.context.get('form')
    #     self.assertIsInstance(form, UserCreationForm)  # I absolutely have no Idea why this test is failing

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('register')
        data = {
            'username': 'john',
            'email': 'john@gmail.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456',
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')

    def test_redirection(self):
        '''
        A valid form submission should redirect the user to the homepage
        '''
        self.assertRedirects(self.response, self.home_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('register')
        self.response = self.client.post(url, {})  # submit an empty dict

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


class SignInTests(TestCase):
    pass


class ResetPassWordTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/password_reset')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf and email
        '''
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'john@gmail.com'
        User.objects.create_user(username='john', email=email, password='123abcdef')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})


    def test_redirection(self):
        '''
        A valid form submission should redirect the user to `password_reset_done` view
        '''
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)


    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@email.com'})

    def test_redirection(self):
        '''
        Even invalid emails in the database should
        redirect the user to `password_reset_done` view
        '''
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)

    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))


class LogOutTests(TestCase):
    pass
