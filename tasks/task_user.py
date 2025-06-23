from celery import shared_task
from .models import TasksWeek
import csv
import json
from taggit.models import Tag


@shared_task
def update_tasks_week():
    # 1. Удаляем старые задачи
    TasksWeek.objects.all().delete()

    # 2. Загружаем новые задачи
    load_new_tasks('data/tasks.json', 'json')


def load_new_tasks(file_path, file_type='csv'):
    """Загружает новые задачи из файла.

    Args:
        file_path: Путь к файлу с задачами.
        file_type: Тип файла ('csv' или 'json').
    """
    TasksWeek.objects.all().delete()  # Удаляем старые задачи

    if file_type == 'csv':
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Пропускаем заголовок

            for row in reader:
                name = row[0]  # Предполагаем, что название задачи находится в первом столбце
                content = row[1]  # Предполагаем, что текст задачи находится во втором столбце
                tags = row[2].split(',')  # Предполагаем, что теги находятся в третьем столбце и разделены запятыми

                task = TasksWeek.objects.create(name=name, content=content)

                # Добавляем теги
                for tag_name in tags:
                    tag_name = tag_name.strip()
                    tag, created = Tag.objects.get_or_create(name=tag_name) #Получаем tag, если он есть, либо создаем
                    task.tags.add(tag)

    elif file_type == 'json':
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                name = item['name']
                content = item['content']
                tags = item['tags']

                task = TasksWeek.objects.create(name=name, content=content)

                # Добавляем теги
                for tag_name in tags:
                    tag_name = tag_name.strip()
                    tag, created = Tag.objects.get_or_create(name=tag_name) #Получаем tag, если он есть, либо создаем
                    task.tags.add(tag)

    else:
        raise ValueError("Неподдерживаемый тип файла")