from pages.base_page import BasePage
from data.endpoints import Endpoints

endpoints = Endpoints()


class OperatorPage(BasePage):
    """Page object для роли Оператор.

    Оператор не имеет бокового меню. Домашняя страница (стартовая точка тестов) —
    страница Отзывов, как у менеджера. Навигация осуществляется через шапку.
    """

    def __init__(self, page):
        # Оператор стартует со страницы Отзывов (как менеджер)
        super().__init__(page, endpoints.FEEDBACK_PAGE_ENDPOINT)

    def open(self):
        """Открывает страницу и дожидается полной загрузки шапки."""
        super().open()
        # Ждём, пока иконка профиля в шапке станет видимой —
        # гарантия того, что страница полностью загружена перед взаимодействием.
        try:
            self.page.locator(".initials__content").wait_for(state="visible", timeout=15000)
        except Exception:
            pass

    # ── Шапка: ссылка «Чаты» ─────────────────────────────────────────────

    def click_chats_link(self, loc):
        """Кликает на ссылку 'Чаты' в шапке."""
        self.click_on_elem(loc.HEADER_CHATS_LINK)

    # ── Шапка: меню профиля ───────────────────────────────────────────────

    def hover_profile_menu(self, loc):
        """Ховер на иконку профиля в шапке для раскрытия выпадающего меню."""
        self.hover_on_elem(loc.HEADER_PROFILE_TRIGGER)

    def click_profile_menu(self, loc):
        """Клик на иконку профиля в шапке для раскрытия выпадающего меню."""
        self.click_on_elem(loc.HEADER_PROFILE_TRIGGER)

    # ── Пункты выпадающего меню профиля ──────────────────────────────────

    def click_my_profile(self, loc):
        """Кликает на 'Мой профиль' в выпадающем меню профиля."""
        self.click_on_elem(loc.PROFILE_MY_PROFILE_BTN)

    def click_support(self, loc):
        """Кликает на 'Написать в поддержку' в выпадающем меню профиля."""
        self.click_on_elem(loc.PROFILE_SUPPORT_BTN)

    def click_history(self, loc):
        """Кликает на 'История обработки' в выпадающем меню профиля."""
        self.click_on_elem(loc.PROFILE_HISTORY_BTN)

    def click_logout(self, loc):
        """Кликает на 'Выход'/'Выйти' в выпадающем меню профиля."""
        self.click_on_elem(loc.PROFILE_LOGOUT_BTN)

    def click_confirm_logout(self, loc):
        """Кликает 'Да' в модальном окне подтверждения выхода."""
        self.click_on_elem(loc.LOGOUT_CONFIRM_YES_BTN)

    # ── Открытие инструкций в новой вкладке ──────────────────────────────

    def wait_for_new_tab_and_get_url(self, loc):
        """Кликает 'Смотреть инструкции', перехватывает новую вкладку, возвращает URL.

        Если ссылка открывается в той же вкладке (нет target="_blank"),
        возвращает URL текущей страницы после навигации.
        """
        try:
            with self.page.context.expect_page(timeout=8000) as new_page_info:
                self.click_on_elem(loc.PROFILE_INSTRUCTIONS_BTN)
            new_page = new_page_info.value
            new_page.wait_for_load_state("domcontentloaded", timeout=30000)
            return new_page.url
        except Exception:
            # Фолбэк: инструкции открылись в текущей вкладке
            try:
                self.page.wait_for_load_state("domcontentloaded", timeout=5000)
            except Exception:
                pass
            return self.page.url

    # ── Шапка: dropdown источника (Маркетплейсы / Карты) ─────────────────

    def click_source_btn(self, loc):
        """Кликает на кнопку-переключатель источника (Маркетплейсы/Карты) в шапке."""
        self.click_on_elem(loc.HEADER_SOURCE_BTN)

    def click_karty_option(self, loc):
        """Кликает на опцию 'Карты' в раскрытом dropdown источника."""
        self.click_on_elem(loc.SOURCE_OPTION_KARTY)

    # ── Утилиты ───────────────────────────────────────────────────────────

    def get_current_url(self):
        """Возвращает текущий URL страницы."""
        return self.page.url
