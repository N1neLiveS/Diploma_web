document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.nav-item');
    const highlightBar = document.querySelector('.highlight-bar');

    // Функция обновления подсветки
    function updateHighlightBar(activeItem) {
        if (!activeItem) {
            highlightBar.style.opacity = '0'; // Скрыть, если нет активного элемента
            return;
        }

        const width = activeItem.offsetWidth;
        const left = activeItem.offsetLeft;
        highlightBar.style.width = `${width}px`;
        highlightBar.style.left = `${left}px`;
        highlightBar.style.opacity = '1'; // Показать подсветку
    }

    // Функция для определения активного элемента
    function getActiveNavItem() {
        const currentPath = window.location.pathname; // Получаем текущий путь

        for (const item of navItems) {
            if (item.classList.contains('active')) {
                continue; // Пропускаем disabled элементы
            }
            const href = item.getAttribute('href');
            if (!href || href === '#') {
                // Если href не указан или равен "#", проверяем по классу active
                if (item.classList.contains('disabled')) {
                    return item;
                }
                continue;
            }
            if (currentPath.startsWith(href)) { // Проверяем, начинается ли текущий путь с href
                return item;
            }
        }
        return null; // Если активный элемент не найден
    }

    // Установка подсветки при загрузке страницы
    const activeNavItem = getActiveNavItem();
    updateHighlightBar(activeNavItem); // Обновляем подсветку

    // Обновление подсветки при клике
    navItems.forEach(item => {
        item.addEventListener('click', (event) => {
            if (item.classList.contains('disabled')) {
                event.preventDefault(); // Предотвращаем переход по ссылке для disabled
                return;
            }
            // Удаляем класс active у всех элементов
            navItems.forEach(navItem => {
                navItem.classList.remove('active');
            });

            item.classList.add('disabled');

            // Обновляем подсветку
            updateHighlightBar(item);
        });
    });
});