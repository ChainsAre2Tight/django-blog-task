from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post, Category
from django.db.models import Q


# Create your views here.
def add_header_to_context(context):
    context['category_list_undivided'] = Category.objects.filter(divided=False)
    context['category_list_divided'] = Category.objects.filter(divided=True)
    return context


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'detailed_post_page'
        add_header_to_context(context)
        return context


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'home_page'
        add_header_to_context(context)
        return context

    def get_queryset(self):
        if self.request.GET.get('q') is not None:
            query = self.request.GET.get("q")
            return Post.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            )
        else:
            return Post.objects.all()


class AboutPageView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'about_page'
        add_header_to_context(context)
        return context


class AboutCategoryView(DetailView):
    template_name = 'about_category_page.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'about_category'
        add_header_to_context(context)
        return context


class CategoryView(ListView):
    model = Post
    template_name = 'category_page.html'

    def get_queryset(self):
        categories = Category.objects.filter(slug=self.kwargs['slug'])[0]
        return Post.objects.filter(category=categories)

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.filter(slug=self.kwargs['slug'])[0]
        add_header_to_context(context)
        return context
