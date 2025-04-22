from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager


class TaskList(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.CharField('Описание', max_length=200)
    poster = models.ImageField('Превью', upload_to='article_images/', blank=True, null=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Task(models.Model):
    task = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='task', verbose_name='Задача')
    name = models.CharField('Название', max_length=200)
    content = CKEditor5Field(verbose_name='Текст задачи', config_name='extends')

    def __str__(self):
        return self.name
