from django.shortcuts import render


def forum(request):
    return render(request, 'forum/forum_layout.html')