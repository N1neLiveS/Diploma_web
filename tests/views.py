from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tests.models import Test, UserTestAttempt, Answer
from .forms import TakeTestForm
from django.utils import timezone
from .utils import update_user_skills
import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def test_list(request):
    tests = Test.objects.all()

    items_per_page = 10
    paginator = Paginator(tests, items_per_page)
    page_number = request.GET.get('page')
    try:
        page_objects = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_objects = paginator.get_page(1)
    except EmptyPage:
        page_objects = paginator.get_page(paginator.num_pages)
    return render(request, 'tests/test_list.html', {'page_objects': page_objects})


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    user = request.user

    # Проверка возможности пересдачи
    last_attempt = UserTestAttempt.objects.filter(user=user, test=test).order_by('-date_taken').first()
    if last_attempt and not last_attempt.can_retake():
        time_difference = timezone.now() - last_attempt.date_taken
        days_left = test.retake_cooldown - time_difference.days
        messages.error(request, f'Вы сможете пересдать этот тест только через {days_left} дней.')
        return redirect('test_list')

    if request.method == 'POST':
        form = TakeTestForm(test, user=user, data=request.POST) # Pass both test and user
        if form.is_valid():
            score = 0
            test_details = {
                'questions': [],
                'total_questions': 0,
                'correct_answers': 0
            }

            # Параметры IRT модели
            DISCRIMINATION = 1.0  # Коэффициент дискриминации
            GUESSING = 0.25  # Вероятность угадывания
            adapted_questions = test.get_questions_for_user(user) # Get the adapted questions

            for question in adapted_questions:
                selected_answer_id = form.cleaned_data.get(f'question_{question.id}')
                test_details['total_questions'] += 1

                if selected_answer_id:
                    try:
                        answer = question.answers.get(id=selected_answer_id)
                        is_correct = answer.is_correct

                        # Обновляем навыки пользователя
                        update_user_skills(user, question, is_correct)

                        if is_correct:
                            # Рассчитываем IRT-балл
                            difficulty = question.difficulty
                            reward = question.reward
                            profile = user.profile
                            topic_scores = profile.get_python_topic_scores()
                            user_ability = topic_scores.get(question.main_tag, 50) if question.main_tag else 50

                            probability = GUESSING + (1 - GUESSING) / (
                                    1 + math.exp(-DISCRIMINATION * (user_ability - difficulty)))
                            question_score = reward * probability
                            score += question_score
                            test_details['correct_answers'] += 1

                        # Сохраняем детали ответа
                        test_details['questions'].append({
                            'id': question.id,
                            'text': question.text,
                            'is_correct': is_correct,
                            'selected_answer': answer.text,
                        })

                    except Answer.DoesNotExist:
                        pass

            # Создаем запись о попытке
            test_attempt = UserTestAttempt.objects.create(
                user=user,
                test=test,
                score=score,
                max_score=test.max_score(),
                details=test_details
            )

            messages.success(request, f'Тест пройден! Ваш результат: {score:.1f} из {test_attempt.max_score}')
            return redirect('test_result', attempt_id=test_attempt.id) # Correct redirect

    else:
        form = TakeTestForm(test, user=user)  # Pass both test and user

    context = {
        'test': test,
        'form': form,
        'is_adapted': request.method == 'GET' and test.get_questions_for_user(user).count() < test.questions.count() # No changes here
    }
    return render(request, 'tests/take_test.html', context)


