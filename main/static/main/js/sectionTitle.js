document.addEventListener('DOMContentLoaded', function() {
    var sectionTitle = document.getElementById('sectionTitle');

    if (sectionTitle) {
        if (window.location.href.includes('/quests')) {
            sectionTitle.textContent = 'Курс Python';
            return; // Выходим из функции
        }
        if (window.location.href.includes('/tasks')) {
            sectionTitle.textContent = 'Задачи Python';
            return;
        }
        if (window.location.href.includes('/tests')) {
            sectionTitle.textContent = 'Тесты';
            return;
        }
        if (window.location.href.includes('/help')) {
            sectionTitle.textContent = 'Помощь по задачам';
            return;
        }
        if (window.location.href.includes('/projects')) {
            sectionTitle.textContent = 'Проекты Python';
            return;
        }
        if (window.location.href.includes('/articles')) {
            sectionTitle.textContent = 'Статьи';
            return;
        }
        if (window.location.href.includes('/reviews')) {
            sectionTitle.textContent = 'Отзывы';
            return;
        }
        if (window.location.href.includes('/forum')) {
            sectionTitle.textContent = 'Форум';
            return;
        }
        if (window.location.href.includes('/me')) {
            sectionTitle.textContent = 'Личный кабинет';
            return;
        }
    }
});