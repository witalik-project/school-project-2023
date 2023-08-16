from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Classes)
admin.site.register(models.PointsLog)
admin.site.register(models.Article)
admin.site.register(models.Photo)
