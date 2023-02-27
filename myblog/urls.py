from django.urls import path
from .views import BlogListView, BlogDetailView, AboutPageView

urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('', BlogListView.as_view(), name='home'),
]