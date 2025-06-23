from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from articles.models import Article
from tests.models import Test
from taggit.models import Tag
User = get_user_model()


class ContentRecommendationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Создаем теги
        self.tag_python = Tag.objects.create(name='Python')
        self.tag_django = Tag.objects.create(name='Django')

        # Создаем тестовый контент
        self.article1 = Article.objects.create(
            title='Python для начинающих',
            content='Базовые концепции Python'
        )
        self.article1.tags.add(self.tag_python)

        self.article2 = Article.objects.create(
            title='Django ORM',
            content='Работа с ORM в Django'
        )
        self.article2.tags.add(self.tag_django)

        # Устанавливаем навыки пользователя
        self.user.profile.python_topic_scores = {'Python': 40, 'Django': 80}
        self.user.profile.save()

    def test_content_recommendations(self):
        self.client.login(username='testuser', password='testpass123')

        # Проверяем, что рекомендации учитывают уровень навыков
        response = self.client.get('/recommendations/')
        self.assertEqual(response.status_code, 200)

        # Проверяем, что Python-статья рекомендована (низкий уровень)
        self.assertContains(response, 'Python для начинающих')

        # Проверяем, что Django-статья не рекомендована (высокий уровень)
        self.assertNotContains(response, 'Django ORM')

        # Проверяем, что рекомендации соответствуют тематикам
        recommended_tags = [tag.name for tag in response.context['recommended_tags']]
        self.assertIn('Python', recommended_tags)
        self.assertNotIn('Django', recommended_tags)
