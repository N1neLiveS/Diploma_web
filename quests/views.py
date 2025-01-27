from django.shortcuts import render


def quests(request):
    return render(request, 'quests/quests.html')


def lectures(request):
    return render(request, 'quests/lectures.html')


def python_basic(request):
    return render(request, 'quests/python_basic_layout.html')
