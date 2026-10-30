from django.shortcuts import render, get_object_or_404, redirect
from . import models, forms


def create_blog_view(request):
    if request.method == "POST":
        form = forms.BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/blog_list/')

    else:
        form = forms.BlogForm()

    return render(request, 'create_blog.html', {'form': form})

def update_blog(request, id):
    blog_id = get_object_or_404(models.Blog, id=id)
    if request.method == "POST":
        form = forms.BlogForm(request.POST, request.FILES, instance=blog_id)
        if form.is_valid():
            form.save()
            return redirect('/blog_list/')
    else:
        form = forms.BlogForm(instance=blog_id)

    return render(request, 'update_form.html', {'form': form})


def delete_blog_view(request, id):
    blog_id = get_object_or_404(models.Blog, id=id)
    blog_id.delete()
    return redirect('/blog_list/')



def blog_list_view(request):
    if request.method == 'GET':
        blog = models.Blog.objects.all().order_by('-id')
    return render(request, template_name='blog_list.html', context={'blog': blog})


def blog_detail_view(request, id):
    if request.method == "GET":
        blog_id = get_object_or_404(models.Blog, id=id)
    return render(request, template_name='blog_detail.html', context={'blog_id': blog_id})

