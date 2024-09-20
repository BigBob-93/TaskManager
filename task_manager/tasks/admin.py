from django.contrib import admin

from .models.task import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
