from django.shortcuts import render, get_object_or_404
from .models import Blog


def blog_list(request):
    blogs = Blog.objects.all()

    return render(request, 'blog/list.html', {
        'blogs': blogs
    })


def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)

    blog.views += 1
    blog.save()

    return render(request, 'blog/detail.html', {
        'blog': blog
    })