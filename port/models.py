from django.db import models
from django.utils.text import slugify
from django.conf import settings
from ckeditor.fields import RichTextField
from portfolio.settings import FIREBASE_STORAGE as fire_storage
from django.core.files.storage import default_storage


def upload_path(instance, filename):
    return f"{instance.gallery.project}/{filename}"


class BlogArticles(models.Model):

    title = models.CharField(max_length=100)
    details = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    description = RichTextField()

    def serialize(self):
        data = {
            'title': self.title,
            'description': self.description,
            'details': self.details,
            'slug': self.slug,
            'main_image': self.gallery.images.get(main=True).serialize(),
            'other_images': [image.serialize() for image in self.gallery.images.filter(main = False)],
        }

        return data

    def __str__(self):
        return self.title

class Project(models.Model):

    title = models.CharField(max_length=100)
    details = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True, unique=True)
    description = RichTextField()
    live_url = models.TextField()
    github_url = models.TextField()

    def serialize(self):
        data = {
            'title': self.title,
            'content': self.description,
            'description': self.details,
            'slug': self.slug,
            'main_image': self.gallery.images.get(main=True).serialize(),
            'other_images': [image.serialize() for image in self.gallery.images.filter(main = False)],
            'live_url': self.live_url,
            'github_url': self.github_url
        }
        return data

    def __str__(self):
        return self.title


class Gallery(models.Model):
    project = models.OneToOneField(
        Project, on_delete=models.CASCADE, related_name='gallery')


def __str__(self):
    return self.project


class Image(models.Model):
    image = models.ImageField(upload_to=upload_path)
    main = models.BooleanField(default=False)
    gallery = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, related_name='images')
    caption = models.CharField(max_length=100, blank=True)
    publicUrl = models.TextField(default='')

    def saveToCloud(self):
        self.save()  # this first saves the image to the database
        file = self.image
        # saves the file to the default storage
        default_storage.save(file.name, file)
        # puts the file in firebase storage
        stuff = fire_storage.child(
            "Project Images/" + file.name).put("media/" + file.name)
        self.publicUrl = fire_storage.child(
            "Project Images/" + file.name).get_url(stuff['downloadTokens'])
        self.save()

    def serialize(self):

      image_details = {
        'imageURL': self.publicUrl,
        'isPrimaryImage': self.main,
        'project': self.gallery.project.title
      }
    
      return image_details


def __str__(self):
    if self.main:
        return self.gallery.project.title + " (Main)"
    return self.gallery.project.title
