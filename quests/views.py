from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def quests(request):
    return render(request, 'quests/quests.html')


def lectures(request):
    return render(request, 'quests/lectures.html')


@login_required  # Только авторизованные пользователи могут создавать посты
def python_basic(request):
    return render(request, 'quests/python_basic_layout.html')
