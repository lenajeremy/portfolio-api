from django.contrib import admin
from .models import *
from ckeditor.widgets import CKEditorWidget
from django import forms
# Register your models here.

class ProjectAdminForm(forms.ModelForm):
    description = forms.CharField(widget = CKEditorWidget)
    class Meta:
        model = Project
        fields = '__all__'

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm

admin.site.register(Project, ProjectAdmin)
admin.site.register(Gallery)
admin.site.register(Image)
