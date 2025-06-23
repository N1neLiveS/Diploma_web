from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager


class Lecture(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.CharField('Описание', max_length=200)
    content = CKEditor5Field(verbose_name='Полное описание', config_name='extends')
    poster = models.ImageField('Превью', upload_to='article_images/', blank=True, null=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Лекция'
        verbose_name_plural = 'Лекции'