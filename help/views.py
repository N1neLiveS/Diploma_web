from django.shortcuts import render


def helps(request):
    return render(request, 'help/help_layout.html')


def create_question(request):
    return render(request, 'help/create_question.html')
