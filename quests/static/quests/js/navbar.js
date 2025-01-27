document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.nav-item');
    const highlightBar = document.querySelector('.highlight-bar');

    // Функция обновления подсветки
    function updateHighlightBar(activeItem) {
        const width = activeItem.offsetWidth;
        const left = activeItem.offsetLeft;
        highlightBar.style.width = `${width}px`;
        highlightBar.style.left = `${left}px`;
    }

    // Устанавливаем подсветку активного элемента
    navItems.forEach(item => {

        item.addEventListener('click', () => {
            navItems.forEach(navItem => navItem.classList.remove('active'));
            item.classList.add('active');
            updateHighlightBar(item);
        });
    });

    // Установка подсветки при загрузке страницы
    const path = window.location.pathname; // Получаем путь текущего URL
    navItems.forEach(item => {
        if (path.includes(item.getAttribute('href'))) { // Проверяем путь
            item.classList.add('active'); // Устанавливаем активный класс
            updateHighlightBar(item); // Обновляем подсветку
        }
    });
});