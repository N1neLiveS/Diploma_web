from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lecture
from tests.models import Test
from tasks.models import TaskList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def quests(request):
    return render(request, 'quests/quests.html')


def lectures_home(request):
    lectures = Lecture.objects.all()

    items_per_page = 12
    paginator = Paginator(lectures, items_per_page)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.get_page(1)
    except EmptyPage:
        page_objects = paginator.get_page(paginator.num_pages)
    return render(request, 'quests/lectures.html', {'page_objects': page_objects})


@login_required  # Только авторизованные пользователи могут создавать посты
def python_basic(request):
    lectures = Lecture.objects.all()
    tests = Test.objects.all()
    tasks = TaskList.objects.all()
    return render(request, 'quests/python_basic_layout.html', {'lectures': lectures, 'tests': tests, 'tasks': tasks})


@login_required
def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    return render(request, 'quests/lectures_detail.html', {'lecture': lecture})
