from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, FormView
from .models import Post, Category, Image
from django.db.models import Q
from .forms import NewUserForm, ImageForm
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .view_functions import add_header_to_context

PPP_list = [1, 2, 5, 10]
default_ppp = 5


class BlogDetailView(DetailView):
    model = Post
    template_name = 'detail_pages/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'detailed_post_page'
        add_header_to_context(context)
        return context


class BlogListView(ListView):
    model = Post
    template_name = 'list_pages/home.html'
    paginate_by = default_ppp

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'home_page'
        add_header_to_context(context)
        context['ppp_list'] = PPP_list
        try:
            context['current_ppp'] = int(self.request.session['ppp'])
        except KeyError:
            context['current_ppp'] = default_ppp
        return context

    def get_paginate_by(self, *args, **kwargs):
        try:
            return self.request.session['ppp']
        except KeyError:
            return super().get_paginate_by(*args, **kwargs)

    def get_queryset(self):
        if self.request.GET.get('ppp') is not None:
            self.request.session['ppp'] = self.request.GET.get('ppp')
        if self.request.GET.get('q') is not None:
            query = self.request.GET.get("q")
            objects = Post.objects.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            ).order_by('id')
            return objects
        else:
            return Post.objects.all()


class AboutPageView(TemplateView):
    template_name = 'detail_pages/about.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'about_page'
        add_header_to_context(context)
        return context


class AboutCategoryView(DetailView):
    template_name = 'detail_pages/about_category_page.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'about_category'
        add_header_to_context(context)
        return context


class CategoryView(ListView):
    model = Post
    template_name = 'list_pages/category_page.html'
    paginate_by = default_ppp

    def get_queryset(self):
        if self.request.GET.get('ppp') is not None:
            self.request.session['ppp'] = self.request.GET.get('ppp')
        categories = Category.objects.filter(slug=self.kwargs['slug'])[0]
        return Post.objects.filter(category=categories)

    def get_paginate_by(self, *args, **kwargs):
        try:
            return self.request.session['ppp']
        except KeyError:
            return super().get_paginate_by(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.filter(slug=self.kwargs['slug'])[0]
        add_header_to_context(context)
        context['ppp_list'] = PPP_list
        try:
            context['current_ppp'] = int(self.request.session['ppp'])
        except KeyError:
            context['current_ppp'] = default_ppp

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
    return render(request=request, template_name="user_interface/register_page.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"???? ?????????? ?????? {username}.")
                return redirect("/")
            else:
                messages.error(request, "???????????????????????? ?????? ???????????????????????? ?????? ????????????")
        else:
            messages.error(request, "???????????????????????? ?????? ???????????????????????? ?????? ????????????")
    form = AuthenticationForm()
    return render(request=request, template_name="user_interface/login_page.html", context={"login_form": form})


def logout_view(request):
    logout(request)
    return redirect('/')


def profile_redirect(request):
    if request.user.is_authenticated:
        userid = request.user.id
        return redirect(f'./{userid}')
    else:
        return redirect('login')


class ImageUploadView(FormView):
    form_class = ImageForm
    template_name = 'user_interface/upload.html'
    success_url = '/'
    image = None

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = self.request.user
            instance.save()
            image_object = form.instance
            self.image = image_object
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        if self.image is not None:
            context['img'] = self.image
        else:
            context['img'] = ''
        return context


class ProfileView(DetailView):
    model = User
    template_name = 'user_interface/profile_page.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'detailed_post_page'
        context['images'] = Image.objects.filter(author_id=self.object.id)
        add_header_to_context(context)
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'list_pages/category_list_page.html'
    paginate_by = default_ppp

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['active_tab_name'] = 'category_list'
        add_header_to_context(context)
        context['ppp_list'] = PPP_list
        try:
            context['current_ppp'] = int(self.request.session['ppp'])
        except KeyError:
            context['current_ppp'] = default_ppp
        return context

    def get_paginate_by(self, *args, **kwargs):
        try:
            return self.request.session['ppp']
        except KeyError:
            return super().get_paginate_by(*args, **kwargs)

    def get_queryset(self):
        if self.request.GET.get('ppp') is not None:
            self.request.session['ppp'] = self.request.GET.get('ppp')
        return Category.objects.all()
