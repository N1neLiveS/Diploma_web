from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Question(models.Model):
    STATUS_CHOICES = [
        ('discussing', 'Обсуждается'),
        ('resolved', 'Решено'),
    ]

    # Связь с пользователем (автором вопроса)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    # Заголовок вопроса
    title = models.CharField('Название', max_length=200)

    # Текст вопроса
    content = CKEditor5Field(verbose_name='Текст вопроса', config_name='extends')

    # Дата создания вопроса (автоматически добавляется при создании)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    # Счётчик просмотров
    views = models.IntegerField('Просмотры', default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='discussing')

    def __str__(self):
        return self.title

    # Метод для увеличения счётчика просмотров
    def increment_views(self):
        self.views += 1
        self.save()

    @property
    def comments_count(self):
        return self.question_comments.count()

    def can_delete(self, user):
        return self.author == user

    class Meta:
        verbose_name = 'Вопрос_пользователя'
        verbose_name_plural = 'Вопросы_пользователей'


class Comment(models.Model):
    # Связь с вопросом (Question)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_comments')

    # Связь с пользователем (автором комментария)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_comments')

    # Текст комментария
    content = models.TextField(max_length=200)

    # Дата создания комментария
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author.username} к вопросу '{self.question.title}'"

    class Meta:
        verbose_name = 'Комментарий Помощи'
        verbose_name_plural = 'Комментарии Помощи'

