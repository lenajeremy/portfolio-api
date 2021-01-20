from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'homepage'),
    path('admin/new_project/', views.new_project, name = 'new_project'),
    path('<str:project>/', views.project, name = 'project')
]


