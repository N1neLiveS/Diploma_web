document.addEventListener('DOMContentLoaded', function() {
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebar = document.getElementById('sidebar');

  console.log("Кнопка sidebar-toggle:", sidebarToggle);
  console.log("Боковое меню sidebar:", sidebar);

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function() {
      if (sidebar.style.display === 'none') {
        sidebar.style.display = 'block';

      } else {
        sidebar.style.display = 'none';

      }
    });
  } else {
    console.error("Не удалось найти кнопку или боковое меню.");
  }
});