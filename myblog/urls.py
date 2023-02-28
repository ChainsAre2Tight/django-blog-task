from django.urls import path
from .views import BlogListView, BlogDetailView, AboutPageView, AboutCategoryView, CategoryView

urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('', BlogListView.as_view(), name='home'),
    path('category/<slug:slug>/about', AboutCategoryView.as_view(), name='about_category'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
]
