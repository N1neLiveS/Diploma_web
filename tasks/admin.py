from django.contrib import admin
from .models import Task, TaskList, TasksWeek


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(TasksWeek)