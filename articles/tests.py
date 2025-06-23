from django.test import TestCase, LiveServerTestCase


class MobileLayoutTests(LiveServerTestCase):
    def test_mobile_menu(self):
        driver = webdriver.Chrome()
        driver.set_window_size(375, 812)  # iPhone X размер

        driver.get(self.live_server_url)
        menu_button = driver.find_element(By.CSS_SELECTOR, '.menu-toggle')

        # Проверяем, что меню скрыто на мобильных
        with self.assertRaises(NoSuchElementException):
            driver.find_element(By.CSS_SELECTOR, 'aside.desktop-nav')

        # Проверяем работу бургер-меню
        menu_button.click()
        mobile_menu = driver.find_element(By.CSS_SELECTOR, 'aside.mobile-nav')
        self.assertTrue(mobile_menu.is_displayed())

        driver.quit()