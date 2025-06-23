from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, CommentForm
from .models import Question, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def helps_forum(request):
    questions = Question.objects.all().order_by('-created_at')

    items_per_page = 10
    paginator = Paginator(questions, items_per_page)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.get_page(1)
    except EmptyPage:
        page_objects = paginator.get_page(paginator.num_pages)
    return render(request, 'help/help_layout.html', {'page_objects': page_objects})


@login_required  # Только авторизованные пользователи могут создавать посты
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # Устанавливаем автора поста
            question.save()
            return redirect('question_detail', question_id=question.id)  # Перенаправляем на страницу поста
    else:
        form = QuestionForm()
    return render(request, 'help/create_question.html', {'form': form})


def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # Получаем список просмотренных постов из сессии
    viewed_questions = request.session.get('viewed_questions', [])

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.author = request.user
            comment.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = CommentForm()

    # Если пост ещё не был просмотрен
    if question_id not in viewed_questions:
        question.increment_views()  # Увеличиваем счётчик просмотров
        viewed_questions.append(question_id)  # Добавляем пост в список просмотренных
        request.session['viewed_questions'] = viewed_questions  # Обновляем сессию

    return render(request, 'help/question_detail.html', {'question': question, 'form': form})


@login_required
def question_delete(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if question.can_delete(request.user):  # Проверяем, является ли пользователь автором
        if request.method == 'POST':
            question.delete()
            return redirect('help')  # Перенаправляем на список вопросов после удаления
    return redirect('question_detail', pk=question_id)


@login_required
def question_update_status(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')  # Получаем новый статус из POST-запроса
        if new_status in [choice[0] for choice in Question.STATUS_CHOICES]:  # Проверяем, что статус валидный
            question.status = new_status
            question.save()
            return redirect('question_detail', question_id=question.id)  # Перенаправляем на страницу детали вопроса
    return redirect('question_detail', question_id=question.id)
