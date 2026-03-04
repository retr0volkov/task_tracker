from django.contrib import admin
from .models import Task, Worker, Stage, Comment

# Register your models here.
admin.site.register(Task)
admin.site.register(Worker)
admin.site.register(Stage)
admin.site.register(Comment)