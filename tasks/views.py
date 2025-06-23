from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TaskList, Task, TasksWeek
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.models import Profile
from django.utils import timezone


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


@login_required
def task_detail(request, task_list_id):
    task_list = get_object_or_404(TaskList, id=task_list_id)
    tasks = Task.objects.filter(task=task_list)
    return render(request, 'tasks/task_detail.html', {'task_list': task_list, 'tasks': tasks})


def my_tasks_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    # Проверяем, нужно ли обновить задачи (например, если прошла неделя с момента последнего обновления)
    if should_update_tasks(profile):
        update_tasks_for_user(profile)

    tasks = profile.tasks.all()  # Получаем задачи пользователя
    print(tasks)
    context = {'tasks': tasks}
    return render(request, 'tasks/my_tasks.html', context)


def should_update_tasks(profile):
    # Логика проверки необходимости обновления задач
    #  Например, проверяем дату последнего обновления
    last_updated = getattr(profile, 'last_tasks_update', None) # Получаем дату последнего обновления
    if last_updated is None:
        return True # Если задач ещё не было, то надо обновить
    # Проверяем, прошла ли неделя с момента последнего обновления
    return (timezone.now() - last_updated).days >= 7


def update_tasks_for_user(profile):
    # 1. Определяем темы, в которых пользователь слаб
    weak_topics = get_weak_topics_for_user(profile.user)

    # 2. Выбираем новые задачи
    from taggit.models import Tag
    weak_topic_tags = Tag.objects.filter(name__in=weak_topics)
    new_tasks = TasksWeek.objects.filter(tags__in=weak_topic_tags).order_by('?')[:5]

    # 3. Обновляем задачи пользователя
    profile.tasks.set(new_tasks)  # Заменяем старые задачи новыми

    # 4. Сохраняем дату обновления
    profile.last_tasks_update = timezone.now()
    profile.save()


def get_weak_topics_for_user(user):
    # Твоя логика определения слабых тем пользователя
    user_profile = user.profile
    user_topic_scores = user_profile.get_python_topic_scores()
    user_topic_scores = user_topic_scores
    weak_topics = [topic for topic, score in user_topic_scores.items() if score is not None and score < 4]
    print(weak_topics)
    return weak_topics