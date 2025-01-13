$(document).ready(function() {
    $(".collapsible").each(function(index) {
        var $collapsible = $(this);
        var $content = $collapsible.find('.collapsible-content');

        // Открыть первый элемент при загрузке страницы
        if (index === 0) {
            $collapsible.addClass('open');
            $content.slideDown();
        }

        $collapsible.find('.collapsible-header').click(function() {
            // Проверка, если клик был на открытом элементе, игнорировать действие
            if ($collapsible.hasClass('open')) {
                return;
            }

            $collapsible.addClass('open');
            $content.slideDown();
            $collapsible.siblings('.collapsible').removeClass('open').find('.collapsible-content').slideUp();
        });
    });
});