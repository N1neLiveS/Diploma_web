from django.db import models
from django.contrib.auth.models import User
import json
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from tasks.models import TasksWeek


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    python_topic_scores = models.TextField(default='{}')
    tasks = models.ManyToManyField(TasksWeek, blank=True, verbose_name='Задачи на неделю')
    last_tasks_update = models.DateTimeField(blank=True, null=True, verbose_name="Последнее обновление задач")

    def __str__(self):
        return f"Profile of {self.user.username}"

    def get_python_topic_scores(self):
        """Возвращает словарь с баллами по темам"""
        try:
            return json.loads(self.python_topic_scores)
        except (TypeError, json.JSONDecodeError):
            return {}

    def update_python_topic_scores(self, new_scores):
        """Обновляет баллы по темам"""
        if not isinstance(new_scores, dict):
            raise ValueError("new_scores должен быть словарем")
        self.python_topic_scores = json.dumps(new_scores)
        self.save()

    def get_topic_score(self, topic_name):
        """Возвращает оценку для конкретной темы Python."""
        scores = self.get_python_topic_scores()
        return scores.get(topic_name)  # Возвращает None, если темы нет

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


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

    class Meta:
        verbose_name = 'Рекомендация'
        verbose_name_plural = 'Рекомендации'


class EventLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время показа')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"EventLog for {self.user.username} at {self.timestamp}"

    class Meta:
        verbose_name = 'Лог Ивента'
        verbose_name_plural = 'Логи Ивента'
