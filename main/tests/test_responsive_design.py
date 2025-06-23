from django.test import TestCase, Client
from django.urls import reverse


class ResponsiveDesignTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_mobile_menu_visibility(self):
        # Эмулируем мобильное устройство с шириной экрана <768px
        mobile_ua = (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        )

        response = self.client.get(
            reverse('home'),
            HTTP_USER_AGENT=mobile_ua
        )

        # Проверяем, что меню скрыто (должен быть класс mobile-hidden)
        self.assertContains(response, 'mobile-hidden', html=True)

        # Проверяем отсутствие "прыгающего" контента
        self.assertNotContains(response, 'transition: all 0.5s ease')

    def test_desktop_menu_visibility(self):
        # Эмулируем десктопный браузер
        desktop_ua = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        response = self.client.get(
            reverse('home'),
            HTTP_USER_AGENT=desktop_ua
        )

        # Проверяем, что меню видимо на десктопе
        self.assertNotContains(response, 'mobile-hidden', html=True)