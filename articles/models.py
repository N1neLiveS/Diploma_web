from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField('Заголовок', max_length=200)
    content = CKEditor5Field('Текст статьи', config_name='extends')
    poster = models.ImageField('Превью', upload_to='article_images/', blank=True, null=True)
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    views = models.IntegerField('Просмотры', default=0)
    article_tags = TaggableManager()

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()

    @property
    def comments_count(self):
        return self.article_comments.count()


class ArticleComment(models.Model):
    # Связь с постом
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments')

    # Связь с пользователем (автором комментария)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_comments')

    # Текст комментария
    content = models.TextField(max_length=200)

    # Дата создания комментария
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"
