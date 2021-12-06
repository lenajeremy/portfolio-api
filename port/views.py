from django.http.response import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, reverse
from django.http import Http404, JsonResponse
from .models import Project, Gallery, Image
from django.utils.text import slugify
from portfolio.settings import BASE_DIR
from django.views.static import serve
import os



def index(request):
    return HttpResponseRedirect('https://jeremiah.vercel.app')


def authenticate(request):
    token = get_token(request)
    return JsonResponse({
        'token': token,
        'message': 'successfully generated token'
    }, status = 200)

def get_projects(request):
    projects = [project.serialize() for project in Project.objects.all()]

    return JsonResponse({
        'projects': projects, 
        'project_count': len(projects)
    }, status = 200)


def get_single_project(request, project):
    try:
        project = get_object_or_404(Project, slug=slugify(project)).serialize()

        return JsonResponse(project, status = 200)
    except Http404:
        return JsonResponse({'error': 'Unable to retrieve project'}, status = 404)


def new_project(request):
    if request.method.upper() == "GET":

        return JsonResponse({'error': 'Bad Request. Expected a POST request'}, status = 400)
    else:
        title = request.POST['title']
        description = request.POST['description']
        long_description = request.POST['long_description']
        github_url = request.POST['github_url']
        live_url = request.POST['live_url']
        project = Project.objects.create(title=title, details=description, slug=slugify(
            title), description=long_description, github_url=github_url, live_url=live_url)
        gallery = Gallery.objects.create(project=project)
        primaryimage = request.FILES.get('primaryImage')
        other_pictures = request.FILES.getlist('otherImages')

        primaryImage = Image(gallery=gallery, main=True, image=primaryimage)

        primaryImage.saveToCloud()


        for image in other_pictures:
            modelImage = Image(gallery=gallery, image=image)
            modelImage.saveToCloud()


        return JsonResponse({
            'message': 'Successful', 
            'project': project.serialize()
        }, status = 200)


def contact(request):
    return render(request, 'port/contact.html')


def download_resume(request):

    filepath = os.path.join(BASE_DIR, 'portfolio', 'resume.pdf')
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
