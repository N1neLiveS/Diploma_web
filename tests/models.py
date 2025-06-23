from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Abs
from django.utils import timezone
from taggit.managers import TaggableManager
from django.db.models import Sum, F


class Test(models.Model):
    DIFFICULTY_CHOICES = [
        (1, 'Очень легко'),
        (2, 'Легко'),
        (3, 'Средне'),
        (4, 'Сложно'),
        (5, 'Очень сложно'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название теста')
    description = models.TextField(blank=True, verbose_name='Описание теста')
    min_questions = models.IntegerField(default=10, verbose_name='Минимальное количество вопросов')
    max_questions = models.IntegerField(default=20, verbose_name='Максимальное количество вопросов')
    retake_cooldown = models.IntegerField(default=21, verbose_name='Дней до пересдачи')
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def max_score(self):
        """Максимальный возможный балл за тест"""
        return self.questions.aggregate(total=Sum('reward'))['total'] or 0

    def get_questions_for_user(self, user):
        """
        Возвращает адаптированный набор вопросов для пользователя
        на основе его уровня знаний по темам теста
        """
        from tests.utils import calculate_user_level  # Импорт здесь чтобы избежать циклических импортов

        # Получаем уровень пользователя по темам теста
        user_level = calculate_user_level(user, self.tags.all())

        # Определяем целевую сложность для пользователя
        target_difficulty = self._get_target_difficulty(user_level)

        # Получаем вопросы с фильтрацией по сложности
        questions = self.questions.annotate(
            difficulty_diff=Abs(F('difficulty') - target_difficulty)
        ).order_by('difficulty_diff')[:self.max_questions]

        # Если вопросов меньше минимального - добавляем случайные
        if questions.count() < self.min_questions:
            additional = self.questions.exclude(id__in=[q.id for q in questions]
                                                ).order_by('?')[:self.min_questions - questions.count()]
            questions = list(questions) + list(additional)

        return questions

    def _get_target_difficulty(self, user_level):
        """Определяет целевую сложность вопросов на основе уровня пользователя"""
        # Логика подбора сложности:
        # 0-20 баллов - уровень 1-2
        # 20-40 - уровень 2-3
        # 40-60 - уровень 3
        # 60-80 - уровень 3-4
        # 80-100 - уровень 4-5
        if user_level < 20:
            return 1 + (user_level / 20)  # Плавный рост от 1 до 2
        elif user_level < 40:
            return 2 + ((user_level - 20) / 20)  # От 2 до 3
        elif user_level < 60:
            return 3
        elif user_level < 80:
            return 3 + ((user_level - 60) / 20)  # От 3 до 4
        else:
            return 4 + ((user_level - 80) / 20)  # От 4 до 5

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', verbose_name='Тест')
    text = models.TextField(verbose_name='Текст вопроса')
    difficulty = models.SmallIntegerField(
        choices=Test.DIFFICULTY_CHOICES,
        default=3,
        verbose_name='Сложность вопроса'
    )
    reward = models.IntegerField(default=1, verbose_name='Награда за правильный ответ')
    main_tag = models.CharField(max_length=15, verbose_name='Награда за правильный ответ')
    tags = TaggableManager()

    def __str__(self):
        return f"{self.text[:50]}... (Тест: {self.test.title})"

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    text = models.CharField(max_length=200, verbose_name='Текст ответа')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return f"{self.text[:50]}... ({'✓' if self.is_correct else '✗'})"

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class UserTestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField(verbose_name='Набранный балл')
    max_score = models.FloatField(verbose_name='Максимальный балл')
    date_taken = models.DateTimeField(auto_now_add=True)

    def can_retake(self):
        """Можно ли пересдать тест?"""
        return (timezone.now() - self.date_taken).days >= self.test.retake_cooldown

    def get_percentage(self):
        """Процент правильных ответов"""
        return round((self.score / self.max_score) * 100, 1) if self.max_score else 0

    class Meta:
        ordering = ['-date_taken']
        verbose_name = 'Отчёт теста'
        verbose_name_plural = 'Отчёты тестов'
