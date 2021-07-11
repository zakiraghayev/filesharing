from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from rest_framework import permissions

from .utils import *
# Create your models here.

class PermType(models.Model):
    perm = models.BooleanField(default=False, help_text="False -> can view, True -> can view and comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="myperm")

    def __str__(self):
        return f" {self.user.username} : {self.perm}"


class FileContainer(models.Model):
    """ File container  """
    
    name = models.CharField(max_length=32)
    desc = models.TextField()
    file = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),   upload_to=get_file_path, default="filecontainer/file.pdf")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myfiles")

    permissions = models.ManyToManyField(PermType, blank=True, related_name="filesshared")

    def __str__(self):
        return self.name


    