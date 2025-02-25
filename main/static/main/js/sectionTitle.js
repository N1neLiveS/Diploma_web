document.addEventListener('DOMContentLoaded', function() {
    var sectionTitle = document.getElementById('sectionTitle');
    
    if (sectionTitle) {
        if (window.location.href.includes('/quests')) {
            sectionTitle.textContent = 'Курс Python';
        } else if (window.location.href.includes('/tasks')) {
            sectionTitle.textContent = 'Задачи Python';
        } else if (window.location.href.includes('/tests')) {
            sectionTitle.textContent = 'Тесты';
        } else if (window.location.href.includes('/help')) {
            sectionTitle.textContent = 'Помощь по задачам';
        } else if (window.location.href.includes('/projects')) {
            sectionTitle.textContent = 'Проекты Python';
        } else if (window.location.href.includes('/articles')) {
            sectionTitle.textContent = 'Статьи';
        } else if (window.location.href.includes('/forum')) {
            sectionTitle.textContent = 'Форум';
        }
    }
});