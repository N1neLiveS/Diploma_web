from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    # Связь с пользователем (автором поста)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

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

    # Свойство для подсчёта количества комментариев
    @property
    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    # Связь с постом
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    # Связь с пользователем (автором комментария)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    # Текст комментария
    content = models.TextField()

    # Дата создания комментария
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

