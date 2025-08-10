from django.shortcuts import render
from blog.models import Post, Category
from django.http import Http404
from django.utils import timezone


empty_post = {
    'id': None,
    'location': None,
    'date': None,
    'category': None,
    'text': None,
}


def index(request):
    template = 'blog/index.html'
    post_list = (
        Post.objects
        .filter(is_published__exact=True,
                category__is_published__exact=True,
                created_at__lte=timezone.now())
        .order_by('-created_at')
        .all()[:5]
    )
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'

    try:
        post = Post.objects.get(pk=id,
                                is_published=True,
                                category__is_published=True,
                                created_at__lte=timezone.now())

    except Post.DoesNotExist:
        raise Http404()

    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    try:
        category = (Category.objects.get(slug=category_slug,
                                         is_published=True))

    except Category.DoesNotExist:
        raise Http404()

    post_list = (
        Post.objects
        .filter(is_published__exact=True,
                category__pk__exact=category.pk,
                created_at__lte=timezone.now())
        .all()
    )

    context = {'category': category,
               'post_list': post_list}
    return render(request, template, context)
