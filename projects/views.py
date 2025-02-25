from django.shortcuts import render


def projects(request):
    return render(request, 'projects/projects.html')


def python_django(request):
    return render(request, 'projects/PythonDjango.html')
