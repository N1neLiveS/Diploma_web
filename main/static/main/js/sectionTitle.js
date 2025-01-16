document.addEventListener('DOMContentLoaded', function() {
    var sectionTitle = document.getElementById('sectionTitle');
    
    if (sectionTitle) {
        if (window.location.href.includes('/quests')) {
            sectionTitle.textContent = 'Курс Python';
        } else if (window.location.href.includes('/tasks')) {
            sectionTitle.textContent = 'Задачи';
        } else if (window.location.href.includes('/tests')) {
            sectionTitle.textContent = 'Тесты';
        }
    }
});