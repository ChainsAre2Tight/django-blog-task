from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post, Category


# Create your views here.
class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'detailed_post_page'
        return context


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'home_page'
        return context


class AboutPageView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'about_page'
        return context


class AboutCategoryView(DetailView):
    template_name = 'about_category_page.html'
    model = Category


class CategoryView(ListView):
    model = Post
    template_name = 'category_page.html'

    def get_queryset(self):
        categories = Category.objects.filter(id=self.kwargs['pk'])[0]
        return Post.objects.filter(category=categories)

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.filter(id=self.kwargs['pk'])[0]
        return context
