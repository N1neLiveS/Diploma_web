from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lecture
from tests.models import Test

def quests(request):
    return render(request, 'quests/quests.html')


def lectures_home(request):
    lectures = Lecture.objects.all()
    return render(request, 'quests/lectures.html', {'lectures': lectures})


@login_required  # Только авторизованные пользователи могут создавать посты
def python_basic(request):
    lectures = Lecture.objects.all()
    tests = Test.objects.all()
    return render(request, 'quests/python_basic_layout.html', {'lectures': lectures, 'tests': tests})


@login_required
def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    return render(request, 'quests/lectures_detail.html', {'lecture': lecture})
