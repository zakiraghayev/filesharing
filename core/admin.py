from django.contrib import admin
from .models import FileContainer, PermType, Comments
# Register your models here.

admin.site.register(FileContainer)
admin.site.register(PermType)
admin.site.register(Comments)
