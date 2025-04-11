from django.db import models
from django.contrib.auth.models import User
import json


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