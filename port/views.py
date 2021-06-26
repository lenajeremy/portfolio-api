from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse, FileResponse
from .models import Project, Gallery, Image
from django.utils.text import slugify
from django import forms
from django.core.files.storage import default_storage
from portfolio.settings import FIREBASE_STORAGE as fire_storage


def index(request):
    context = [project.serialize() for project in Project.objects.all()]
    return render(request, 'port/index.html', context={'projects': context})


def project(request, project):
    try:
        project = get_object_or_404(Project, slug=slugify(project))
        return render(request, 'port/post.html', context={'project': project.serialize()})
    except Http404:
        return HttpResponseRedirect(reverse('homepage'))


def new_project(request):
    if request.method.upper() == "GET":
        
        return render(request, 'port/form.html')
    else:
        title = request.POST['title']
        description = request.POST['description']
        long_description = request.POST['long_description']
        github_url = request.POST['github_url']
        live_url = request.POST['live_url']
        project = Project.objects.create(title=title, details=description, slug=slugify(
            title), description=long_description, github_url=github_url, live_url=live_url)
        gallery = Gallery.objects.create(project=project)
        primaryimage = request.FILES.get('main_picture')
        other_pictures = request.FILES.get('other_pictures')

        primaryImage = Image(gallery=gallery, main=True, image=primaryimage)
        secondaryImage= Image(gallery=gallery, image=other_pictures)
        
        primaryImage.saveToCloud()
        secondaryImage.saveToCloud()
        return HttpResponseRedirect(reverse('homepage'))


def contact(request):
    return render(request, 'port/contact.html')