from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'  # ✅ keep only this

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),  # ✅ homepage
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),  # ✅ create post
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),  # ✅ detail page

    path('login/', auth_views.LoginView.as_view(template_name='blog/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='blog:login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),

]

