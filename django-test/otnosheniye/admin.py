from django.contrib import admin
from . import models
admin.site.register(models.Car)
admin.site.register(models.StateNumberCar)
admin.site.register(models.CommentCar)
admin.site.register(models.CategoryCar)