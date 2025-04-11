from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Test, UserTestAttempt, Answer
from .forms import TakeTestForm
from django.utils import timezone
import datetime
from taggit.models import Tag
import json


@login_required
def test_list(request):
    tests = Test.objects.all()
    return render(request, 'tests/test_list.html', {'tests': tests})


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user = request.user

    # Проверка возможности пересдачи
    last_attempt = UserTestAttempt.objects.filter(user=user, test=test).order_by('-date_taken').first()
    if last_attempt and not last_attempt.can_retake():
        time_difference = timezone.now() - last_attempt.date_taken
        weeks_left = (datetime.timedelta(weeks=3) - time_difference).days // 7
        messages.error(request, f'Вы сможете пересдать этот тест только через {weeks_left} недель.')
        return redirect('test_list')  # Или на страницу с деталями теста

    if request.method == 'POST':
        form = TakeTestForm(test, request.POST)
        if form.is_valid():
            score = 0  # Общий балл за тест
            for question in test.questions.all():
                selected_answer_id = form.cleaned_data.get(f'question_{question.id}')
                if selected_answer_id:
                    try:
                        answer = question.answers.get(id=selected_answer_id)
                        if answer.is_correct:
                            score += question.reward  # Начисляем награду за правильный ответ

                            # Обновляем баллы в профиле пользователя для тегов вопроса
                            user_profile = user.profile
                            topic_scores = user_profile.get_python_topic_scores()

                            for tag in question.tags.names():  # перебираем теги
                                if tag in topic_scores:
                                     if topic_scores[tag] is None:
                                         topic_scores[tag] = question.reward
                                     else:
                                         topic_scores[tag] += question.reward
                                else:
                                    topic_scores[tag] = question.reward

                            user_profile.python_topic_scores = json.dumps(topic_scores)
                            user_profile.save()

                    except Answer.DoesNotExist:
                        pass

            test_attempt = UserTestAttempt.objects.create(user=user, test=test, score=score)
            messages.success(request, f'Тест пройден! Ваш результат: {score}')
            return redirect('test_list')
    else:
        form = TakeTestForm(test)

    return render(request, 'tests/take_test.html', {'test': test, 'form': form})




