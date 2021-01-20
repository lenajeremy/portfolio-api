from django.db import models
from django.utils.text import slugify
from django.conf import settings

# Create your models here.

def upload_path(instance, filename):
  return f"{instance.gallery.project}/{filename}"


class Project(models.Model):
  title = models.CharField(max_length = 100)
  details = models.CharField(max_length = 250)
  slug = models.SlugField(max_length = 250, blank = True)
  description = models.TextField()
  
  def serialize(self):
    data = {'title': self.title, 'details': self.details, 'slug': self.slug, 'main_image': self.gallery.images.get(main = True), 'secondary_image' : self.gallery.images.get(main = False)}
    return data
  
  def __str__(self):
			return self.title

  
class Gallery(models.Model):
  project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name = 'gallery')

def __str__(self):
  return self.project


class Image(models.Model):
  image = models.ImageField(upload_to=upload_path)
  main = models.BooleanField(default = False)
  gallery = models.ForeignKey(Gallery, on_delete = models.CASCADE, related_name = 'images')
  
  def __str__(self):
			return self.image.url
 
  
