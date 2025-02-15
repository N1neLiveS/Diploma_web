from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    # Связь с пользователем (автором поста)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')

    # Заголовок поста
    title = models.CharField('Название', max_length=200)

    # Текст поста
    content = models.TextField('Текст')

    # Дата создания поста (автоматически добавляется при создании)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    # Счётчик просмотров
    views = models.IntegerField('Просмотры', default=0)

    def __str__(self):
        return self.title

    # Метод для увеличения счётчика просмотров
    def increment_views(self):
        self.views += 1
        self.save()

    @property
    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    # Связь с вопросом (Question)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')

    # Связь с пользователем (автором комментария)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_comments')

    # Текст комментария
    content = models.TextField()

    # Дата создания комментария
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author.username} к вопросу '{self.question.title}'"