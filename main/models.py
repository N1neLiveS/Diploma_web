from django.db import models
from django.contrib.auth.models import User
import json
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    python_topic_scores = models.TextField(default='{}')  # JSON в текстовом поле

    def __str__(self):
        return f"Profile of {self.user.username}"

    def get_python_topic_scores(self):
        """Возвращает словарь оценок тем Python."""
        try:
            return json.loads(self.python_topic_scores)
        except json.JSONDecodeError:
            return {}  # Возвращаем пустой словарь при ошибке

    def set_python_topic_score(self, topic_name, score):
        """Устанавливает оценку для темы Python."""
        scores = self.get_python_topic_scores()
        scores[topic_name] = score
        self.python_topic_scores = json.dumps(scores)

    def get_topic_score(self, topic_name):
        """Возвращает оценку для конкретной темы Python."""
        scores = self.get_python_topic_scores()
        return scores.get(topic_name)  # Возвращает None, если темы нет


class EventUser(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    template_name = models.CharField(max_length=200, verbose_name='Шаблон')
    start_date = models.DateTimeField(verbose_name='Дата начала показа')
    end_date = models.DateTimeField(verbose_name='Дата окончания показа')
    tags = TaggableManager() #Темы, связанные с этим эвентом
    priority = models.IntegerField(default=1, verbose_name='Приоритет') #Порядок показа эвентов
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Тип контента')
    object_id = models.PositiveIntegerField(verbose_name='ID объекта')
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title


class EventLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    event = models.ForeignKey('EventUser', on_delete=models.CASCADE, verbose_name='Эвент')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время показа')

    def __str__(self):
        return f'{self.user.username} - {self.event.title} - {self.timestamp}'

    class Meta:
        unique_together = ('user', 'event', 'timestamp')