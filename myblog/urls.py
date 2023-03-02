from django.urls import path
from .views import BlogListView, BlogDetailView, AboutPageView, AboutCategoryView, CategoryView, ProfileView
from .views import register_request, login_request, logout_view

urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('', BlogListView.as_view(), name='home'),
    path('category/<slug:slug>/about', AboutCategoryView.as_view(), name='about_category'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('register', register_request, name='register'),
    path('login', login_request, name='login'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('logout', logout_view, name='logout')
]
