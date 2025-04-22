from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TaskList, Task
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def tasks_list(request):
    tasks = TaskList.objects.all()

    items_per_page = 12
    paginator = Paginator(tasks, items_per_page)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.get_page(1)
    except EmptyPage:
        page_objects = paginator.get_page(paginator.num_pages)
    return render(request, 'tasks/tasks_list.html', {'page_objects': page_objects})


def task_detail(request, task_list_id):
    task_list = get_object_or_404(TaskList, id=task_list_id)
    tasks = Task.objects.filter(task=task_list)
    return render(request, 'tasks/task_detail.html', {'task_list': task_list, 'tasks': tasks})
