from django.shortcuts import render


def forum(request):
    return render(request, 'forum/forum_layout.html')


def create_post(request):
    return render(request, 'forum/create_post.html')
