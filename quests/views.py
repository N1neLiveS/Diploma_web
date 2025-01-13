from django.shortcuts import render


def quests(request):
    return render(request, 'quests/quests.html')
