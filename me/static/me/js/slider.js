 $(document).ready(function(){
      $('.slider').slick({
        dots: true,          // Показывать точки навигации
        infinite: true,      // Бесконечная прокрутка
        speed: 300,          // Скорость анимации
        slidesToShow: 3,      // Количество слайдов для отображения
        slidesToScroll: 1,    // Количество слайдов для прокрутки
        responsive: [
            {
              breakpoint: 1024,
              settings: {
                slidesToShow: 3,
                slidesToScroll: 1,
                infinite: true,
                dots: true
              }
            },
            {
              breakpoint: 600,
              settings: {
                slidesToShow: 2,
                slidesToScroll: 1
              }
            },
            {
              breakpoint: 480,
              settings: {
                slidesToShow: 1,
                slidesToScroll: 1
              }
            }
          ]
      });
    });