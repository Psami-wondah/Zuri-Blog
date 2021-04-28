from django.urls import path
from .views import BlogListView, logout_request, post_detail, \
      BlogUpdateView, BlogDeleteView, signup, login_request, post_form

urlpatterns = [

    #path("password_reset", password_reset_request, name="password_reset"),
    path('logout/', logout_request, name='logout'),
    path('login/', login_request, name='login'),
    path('register/', signup, name='register'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/new/', post_form, name='post_new'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('', BlogListView.as_view(), name='home')
]
