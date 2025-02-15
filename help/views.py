from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, CommentForm
from .models import Question, Comment


def helps_forum(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'help/help_layout.html', {'questions': questions})


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
