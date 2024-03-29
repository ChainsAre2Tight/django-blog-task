from django.urls import path
from .views import BlogListView, BlogDetailView, AboutPageView, AboutCategoryView, CategoryView, ProfileView, \
    CategoryListView, ImageUploadView, UserListView
from .views import register_request, login_request, logout_view, profile_redirect

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('category/', CategoryListView.as_view(), name='category_browser'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('category/<slug:slug>/about', AboutCategoryView.as_view(), name='about_category'),
    path('profile/', profile_redirect),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('logout', logout_view, name='logout'),
    path('register', register_request, name='register'),
    path('login', login_request, name='login'),
    path('upload', ImageUploadView.as_view(), name='upload'),
    path('users', UserListView.as_view(), name='users'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
