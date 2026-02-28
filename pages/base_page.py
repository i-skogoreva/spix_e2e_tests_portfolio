class BasePage:

    def __init__(self, page, url):
        self.page = page
        self.url = url

    def open(self):
        self.page.goto(self.url)
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass  # если networkidle не наступил — всё равно продолжаем
        # Закрываем попап «Быть в курсе новостей и акций», если он появился
        try:
            popup = self.page.locator(
                "button:has-text('В другой раз'), button:has-text('Согласен')"
            ).first
            popup.wait_for(state="visible", timeout=3000)
            popup.click()
            self.page.wait_for_timeout(300)
        except Exception:
            pass

    def fill_text(self, loc, text_data):
        self.page.locator(loc).fill(text_data)

    def click_on_elem(self, loc):
        self.page.locator(loc).click()

    def get_text(self,loc):
        text = self.page.locator(loc).text_content()
        return text

    def get_all_text(self, loc):
        text = self.page.locator(loc).all_text_contents()
        return text

    def wait_url(self, url):
        self.page.wait_for_url(url)

    def wait_url_contains(self, url_fragment, timeout=20000):
        """Ждёт пока URL содержит url_fragment.

        Гибридный подход:
        1. wait_for_url('commit', 2.5s) — ловит быструю HTTP-навигацию через commit-событие
           (работает даже если после commit следует SPA-редирект на другой URL,
           например клик «Чаты» делает HTTP-запрос, а потом SPA редиректит обратно).
        2. Проверяем page.url — за 2.5с Playwright успевает обработать
           CDP-событие от SPA history.pushState, произошедшего ДО вызова шага 1.
        3. wait_for_function — опрашивает window.location.href каждые ~100мс.
           Ловит медленный SPA pushState (Настройки, Товары, Места, Карты),
           который происходит ПОСЛЕ таймаута шага 1.
        """
        # Шаг 1: быстрая HTTP-навигация (commit-событие, ≤ 2.5s)
        try:
            self.page.wait_for_url(f"**{url_fragment}**", wait_until='commit', timeout=2500)
            return
        except Exception:
            pass

        # Шаг 2: SPA pushState, произошедший до вызова wait_for_url
        if url_fragment in self.page.url:
            return

        # Шаг 3: медленный SPA pushState или медленная HTTP-навигация
        remaining = max(timeout - 2500, 5000)
        try:
            self.page.wait_for_function(
                "fragment => window.location.href.includes(fragment)",
                arg=url_fragment,
                timeout=remaining,
            )
        except Exception:
            if url_fragment not in self.page.url:
                raise

    def get_attribute(self, loc, attribute):
        return self.page.locator(loc).get_attribute(attribute)

    def hover_on_elem(self, loc):
        self.page.locator(loc).hover()

    def wait_locator(self, locator, timeout=15000):
        self.page.locator(locator).wait_for(
        state="visible",
        timeout=timeout
        )