from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from .models import Project, Gallery, Image
from django.utils.text import slugify

# Create your views here.
def index(request):
  return render(request, 'port/index.html', context = {'projects': [project.serialize() for project in Project.objects.all()]})

def project(request, project):
  try:
    project = get_object_or_404(Project, slug = slugify(project))
    return render(request, 'port/post.html', context = {'project': project.serialize()})
  except Http404:
    return HttpResponseRedirect(reverse('homepage'))
  
def new_project(request):
  if request.method.upper() == "GET":
    return render(request, 'port/form.html')  
  else:
    title = request.POST['title']
    description = request.POST['description']
    long_description = request.POST['long_description']
    primaryimage = request.FILES.get('main_picture')
    other_pictures = request.FILES.get('other_pictures') 
    project = Project.objects.create(title = title, details = description, slug = slugify(title), description = long_description)
    gallery = Gallery.objects.create(project = project)
    Image.objects.create(gallery = gallery, main = True, image = primaryimage)
    Image.objects.create(gallery = gallery, image = other_pictures)
    return HttpResponseRedirect(reverse('homepage'))

def contact(request):
  return render(request, 'port/contact.html')