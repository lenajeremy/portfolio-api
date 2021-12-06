from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('authenticate/', views.authenticate, name = 'authenticate'),
    path('get_projects/', views.get_projects, name = 'get_projects'),
    path('add_project/', views.new_project, name = 'new_project'),
    path('contact/', views.contact, name = 'contact'),
    path('download_resume/', views.download_resume, name = 'download_resume'),
    path('project/<str:project>/', views.get_single_project, name = 'project')
]


