from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models

from .utils import *
# Create your models here.

class PermType(models.Model):
    perm = models.BooleanField(default=False, help_text="False -> can view, True -> can view and comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="myperm")

    def __str__(self):
        return f" {self.user.username} : {self.perm}"


class Comments(models.Model):
    """ Comments Model contains comment made): """
    owner = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="mycomments")
    text  = models.TextField()

    def __str__(self):
        return "Comment by "+self.owner.username
       


class FileContainer(models.Model):
    """ File container  """
    
    name = models.CharField(max_length=32)
    desc = models.TextField()
    file = models.FileField(storage=FileSystemStorage(location=settings.MEDIA_ROOT),   upload_to=get_file_path, default="filecontainer/file.pdf")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="myfiles")

    permissions = models.ManyToManyField(PermType, blank=True, related_name="filesshared")

    # the field name should be comments
    comments = models.ManyToManyField(Comments, related_name="fileoncomment")

    def __str__(self):
        return self.name

    def has_perm_view(self, user):
        """ If return True means user can view,
         else no access at all"""
        try:
            perm = self.permissions.get(user=user)
            return perm.perm == False or perm.perm == True
        except:
            return False
    
    def has_perm_comment(self, user):
        """ If return True means user can comment,
         else can view or no access at all"""
        try:
            perm = self.permissions.get(user=user)
            return perm.perm or self.owner == user
        except:
            return False or self.owner == user

    def comment(self, user, text):
        if self.has_perm_comment(user):
            self.comments.create(owner=user, text=text)
            self.save()
            return True
        return False


    