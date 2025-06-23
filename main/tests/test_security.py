from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from articles.models import Article

User = get_user_model()


class XSSProtectionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
        )

    def test_xss_in_article_content(self):
        self.client.login(username='testuser', password='testpass123')

        # Пытаемся создать статью с XSS-кодом
        xss_payload = "<script>alert('XSS')</script>"
        response = self.client.post(
            '/articles/create/',
            {
                'title': 'Тест XSS',
                'content': xss_payload,
                'tags': 'security'
            }
        )

        # Проверяем, что статья создана
        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(title='Тест XSS')

        # Проверяем, что XSS-код экранирован
        response = self.client.get(f'/articles/{article.id}/')
        self.assertNotContains(response, '<script>')
        self.assertContains(response, '&lt;script&gt;')  # Проверяем экранированные символы

    def test_xss_in_comment(self):
        self.client.login(username='testuser', password='testpass123')

        # Пытаемся оставить комментарий с XSS
        xss_payload = "<img src=x onerror=alert('XSS')>"
        response = self.client.post(
            '/articles/1/comment/',
            {'text': xss_payload}
        )

        # Проверяем, что комментарий добавлен
        self.assertEqual(response.status_code, 302)

        # Проверяем отображение комментария
        response = self.client.get('/articles/1/')
        self.assertNotContains(response, 'onerror=')
        self.assertContains(response, '&lt;img src=x onerror=alert(&#39;XSS&#39;)&gt;')