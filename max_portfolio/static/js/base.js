// Главный JS-файл фронтенда.
// Отвечает за:
// 1) переключение светлой/тёмной темы;
// 2) анимацию счётчиков на главной;
// 3) анимацию полос навыков.
(function () {
  // Ключ localStorage для хранения выбранной пользователем темы.
  const storageKey = "max_portfolio_theme";
  const root = document.documentElement;
  const toggle = document.getElementById("themeToggle");

  // Функция применения темы к документу.
  const applyTheme = (theme) => {
    root.setAttribute("data-theme", theme);
    const icon = toggle?.querySelector(".theme-icon");
    if (icon) {
      icon.textContent = theme === "dark" ? "☀️" : "🌙";
    }
  };

  // При загрузке страницы восстанавливаем последнюю выбранную тему.
  const saved = localStorage.getItem(storageKey) || "light";
  applyTheme(saved);

  // Обработчик кнопки переключения темы.
  toggle?.addEventListener("click", () => {
    const current = root.getAttribute("data-theme") || "light";
    const next = current === "light" ? "dark" : "light";
    localStorage.setItem(storageKey, next);
    applyTheme(next);
  });

  // Анимация цифровых счётчиков в статистических карточках.
  const animateCounter = (el) => {
    const target = Number(el.dataset.value || 0);
    const duration = 900;
    const stepTime = 16;
    const totalSteps = Math.max(1, Math.floor(duration / stepTime));
    let step = 0;

    const timer = setInterval(() => {
      step += 1;
      const progress = step / totalSteps;
      el.textContent = String(Math.round(target * progress));
      if (step >= totalSteps) {
        el.textContent = String(target);
        clearInterval(timer);
      }
    }, stepTime);
  };

  document.querySelectorAll(".counter").forEach(animateCounter);

  // Плавная анимация ширины полос навыков.
  document.querySelectorAll(".skill-bar i").forEach((bar) => {
    requestAnimationFrame(() => {
      bar.style.width = bar.style.getPropertyValue("--w") || "0%";
    });
  });
})();