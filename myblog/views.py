from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post


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
