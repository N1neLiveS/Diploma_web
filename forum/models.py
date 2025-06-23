from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField('Название', max_length=200)
    content = CKEditor5Field(verbose_name='Полное описание', config_name='extends')
    created_at = models.DateTimeField('Дата', auto_now_add=True)
    views = models.IntegerField('Просмотры', default=0)

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()

    @property
    def comment_count(self):
        return self.comments.count()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    # Связь с постом
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    # Связь с пользователем (автором комментария)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    # Текст комментария
    content = models.TextField(max_length=200)

    # Дата создания комментария
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    class Meta:
        verbose_name = 'Комментарий Поста'
        verbose_name_plural = 'Комментрии Поста'



class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
