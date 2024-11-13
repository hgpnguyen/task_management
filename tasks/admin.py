from django.contrib import admin
from .models import Task

# Register Task to admin.
@admin.register(Task)
class TaskModel(admin.ModelAdmin):
    pass