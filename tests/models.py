from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from taggit.managers import TaggableManager


class Test(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название теста')
    description = models.TextField(blank=True, verbose_name='Описание теста')
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', verbose_name='Тест')
    text = models.TextField(verbose_name='Текст вопроса')
    reward = models.IntegerField(default=1, verbose_name='Награда за правильный ответ')
    tags = TaggableManager()

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    text = models.CharField(max_length=200, verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return self.text


class UserTestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    date_taken = models.DateTimeField(auto_now_add=True, verbose_name='Дата сдачи')
    score = models.IntegerField(default=0, verbose_name='Результат') #Можно добавить поле для связи с UserProfile, если это нужно
    # python_topic_scores = models.JSONField(default=dict) #Словарь тем

    def __str__(self):
        return f'{self.user.username} - {self.test.title} - {self.date_taken}'

    def can_retake(self):
        """Проверяет, может ли пользователь пересдать тест."""
        last_attempt = UserTestAttempt.objects.filter(user=self.user, test=self.test).order_by('-date_taken').first()
        if last_attempt:
            time_difference = timezone.now() - last_attempt.date_taken
            return time_difference >= datetime.timedelta(weeks=3)
        return True  # Если не было попыток, можно проходить