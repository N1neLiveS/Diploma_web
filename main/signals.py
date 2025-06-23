from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
import json


# Сигнал для автоматического создания профиля при создании пользователя
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Создает профиль пользователя и инициализирует темы Python."""
    if created:  # Создаётся профиль только при создании пользователя
        Profile.objects.create(user=instance)
        # Инициализируем темы Python
        profile = instance.profile
        initial_scores = {
            'input': None,
            'print': None,
            'for': None,
            'if': None,
            'dict': None,
            'list': None,
            'while': None,
            'def': None,
            'class': None,
            'try': None,
            'except': None,
            'import': None,
            'string': None,
            'integer': None,
            'float': None,
            'boolean': None,
            'files': None,
            'oop': None,
            'decorators': None,
            'generators': None,
        }
        profile.python_topic_scores = json.dumps(initial_scores)
        profile.save()


# Сигнал для автоматического сохранения профиля при сохранении пользователя
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):  # Проверяем, существует ли профиль
        instance.profile.save()


