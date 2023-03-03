from .models import Post, Category


def add_header_to_context(context):
    context['category_list_undivided'] = Category.objects.filter(divided=False)
    context['category_list_divided'] = Category.objects.filter(divided=True)
    return context
