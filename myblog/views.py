from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import Post, Category
from django.db.models import Q
from .forms import NewUserForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .view_functions import add_header_to_context

PPP_list = [1, 2, 5, 10]
default_ppp = 5


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
    paginate_by = default_ppp

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'home_page'
        add_header_to_context(context)
        context['ppp_list'] = PPP_list
        context['current_ppp'] = int(self.request.session['ppp'])
        return context

    def get_paginate_by(self, *args, **kwargs):
        try:
            return self.request.session['ppp']
        except KeyError:
            return super().get_paginate_by(*args, **kwargs)

    def get_queryset(self):
        if self.request.GET.get('ppp') is not None:
            self.request.session['ppp'] = self.request.GET.get('ppp')
        try:
            ppp = self.request.session['ppp']
        except KeyError:
            self.request.session['ppp'] = default_ppp
        if self.request.GET.get('q') is not None:
            query = self.request.GET.get("q")
            objects = Post.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            ).order_by('id')
            return objects
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


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register_page.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы вошли как {username}.")
                return redirect("/")
            else:
                messages.error(request, "Неправильное имя пользователя или пароль")
        else:
            messages.error(request, "Неправильное имя пользователя или пароль")
    form = AuthenticationForm()
    return render(request=request, template_name="login_page.html", context={"login_form": form})


def logout_view(request):
    logout(request)
    return redirect('/')


class ProfileView(DetailView):
    model = User
    template_name = 'profile_page.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'detailed_post_page'
        add_header_to_context(context)
        return context
