from pages.base_page import BasePage
from data.endpoints import Endpoints

endpoints = Endpoints()


class SideMenuPage(BasePage):

    def __init__(self, page):
        super().__init__(page, endpoints.FEEDBACK_PAGE_ENDPOINT)

    def is_sidebar_open(self, loc) -> bool:
        """Проверяет, что боковое меню открыто (класс sidebar with-sidebar)"""
        return self.page.locator(loc.SIDEBAR_OPEN).is_visible()

    def click_menu_item_reviews(self, loc):
        """Кликает на пункт меню 'Отзывы' для раскрытия подменю"""
        self.click_on_elem(loc.MENU_ITEM_REVIEWS)

    def is_submenu_active(self, loc) -> bool:
        """Проверяет, что подменю Отзывы стало активным"""
        return self.page.locator(loc.SUBMENU_ACTIVE).is_visible()

    def click_submenu_item_karty(self, loc):
        """Кликает на пункт подменю 'Карты'"""
        self.click_on_elem(loc.SUBMENU_ITEM_KARTY)

    def is_karty_aria_current(self, loc) -> bool:
        """Проверяет, что пункт 'Карты' стал активным (aria-current='page')"""
        return self.page.locator(loc.KARTY_ARIA_CURRENT).is_visible()

    def setup_skeleton_observer(self, loc):
        """Запускает JS-опрос каждые 5мс для отслеживания скелетона ДО клика"""
        self.page.evaluate(f"""
            () => {{
                window._skeletonAppeared = false;
                if (window._skeletonInterval) clearInterval(window._skeletonInterval);

                window._skeletonInterval = setInterval(() => {{
                    const loader = document.querySelector('{loc.SKELETON}');
                    if (loader) {{
                        const rect = loader.getBoundingClientRect();
                        if (rect.width > 0 && rect.height > 0) {{
                            window._skeletonAppeared = true;
                            clearInterval(window._skeletonInterval);
                        }}
                    }}
                }}, 5);

                setTimeout(() => clearInterval(window._skeletonInterval), 5000);
            }}
        """)

    def check_skeleton_appeared(self):
        """Проверяет что скелетон появлялся после клика"""
        self.page.evaluate("() => clearInterval(window._skeletonInterval)")
        appeared = self.page.evaluate("() => window._skeletonAppeared === true")
        assert appeared, "Скелетон не появился (.loader-wrapper)"

    def click_menu_item_chats(self, loc):
        """Кликает на пункт меню 'Чаты'"""
        self.click_on_elem(loc.MENU_ITEM_CHATS)

    def is_chat_page_open(self, loc) -> bool:
        """Проверяет открытие страницы чатов по наличию заголовка"""
        return self.page.locator(loc.CHAT_PAGE_TITLE).is_visible()

    def is_sidebar_collapsed(self, loc) -> bool:
        """Проверяет что боковое меню схлопнулось (нет класса with-sidebar)"""
        return self.page.locator(loc.SIDEBAR_COLLAPSED).is_visible()

    def expand_sidebar(self, loc):
        """Раскрывает боковое меню, если оно узкое (.sidebar-wrapper.small)"""
        if self.is_sidebar_collapsed(loc):
            self.click_on_elem(loc.SIDEBAR_BURGER)

    def click_menu_item_products(self, loc):
        """Кликает на пункт меню 'Товары'"""
        self.click_on_elem(loc.MENU_ITEM_PRODUCTS)

    def is_products_page_open(self, loc) -> bool:
        """Проверяет открытие страницы Товары по наличию заголовка h1"""
        return self.page.locator(loc.PRODUCTS_PAGE_TITLE).is_visible()

    def click_menu_item_places(self, loc):
        """Кликает на пункт меню 'Места'"""
        self.click_on_elem(loc.MENU_ITEM_PLACES)

    def is_places_page_open(self, loc) -> bool:
        """Проверяет открытие страницы Места по наличию заголовка"""
        return self.page.locator(loc.PLACES_PAGE_TITLE).is_visible()

    def click_menu_item_clients(self, loc):
        """Кликает на пункт меню 'Клиенты'"""
        self.click_on_elem(loc.MENU_ITEM_CLIENTS)

    def is_clients_page_open(self, loc) -> bool:
        """Проверяет открытие страницы Клиенты по наличию заголовка"""
        return self.page.locator(loc.CLIENTS_PAGE_TITLE).is_visible()

    def click_menu_item_analytics(self, loc):
        """Кликает на пункт меню 'Аналитика' для раскрытия подменю"""
        self.click_on_elem(loc.MENU_ITEM_ANALYTICS)

    def is_analytics_submenu_open(self, loc) -> bool:
        """Проверяет наличие подпункта 'Отзывы' в подменю Аналитика"""
        return self.page.locator(loc.ANALYTICS_SUBMENU_REVIEWS).is_visible()

    def click_analytics_submenu_reviews(self, loc):
        """Кликает на подпункт подменю 'Отзывы' в разделе Аналитика"""
        self.click_on_elem(loc.ANALYTICS_SUBMENU_REVIEWS)

    def is_analytics_reviews_active(self, loc) -> bool:
        """Критерий 1: подпункт Отзывы стал активным (router-link-active)"""
        return self.page.locator(loc.ANALYTICS_REVIEWS_ACTIVE).is_visible()

    def is_analytics_reviews_page_open(self, loc) -> bool:
        """Критерий 2: открылась страница Аналитика > Отзывы (analytics-section__header)"""
        return self.page.locator(loc.ANALYTICS_REVIEWS_PAGE_HEADER).is_visible()

    def click_analytics_submenu_processing(self, loc):
        """Кликает на подпункт подменю 'Обработка' в разделе Аналитика"""
        self.click_on_elem(loc.ANALYTICS_SUBMENU_PROCESSING)

    def is_analytics_processing_active(self, loc) -> bool:
        """Критерий 1: подпункт Обработка стал активным (router-link-active)"""
        return self.page.locator(loc.ANALYTICS_PROCESSING_ACTIVE).is_visible()

    def is_analytics_processing_page_open(self, loc) -> bool:
        """Критерий 2: открылась страница Аналитика > Обработка"""
        return self.page.locator(loc.ANALYTICS_PROCESSING_PAGE_HEADER).is_visible()

    def click_analytics_submenu_insights(self, loc):
        """Кликает на подпункт подменю 'Инсайты' в разделе Аналитика"""
        self.click_on_elem(loc.ANALYTICS_SUBMENU_INSIGHTS)

    def is_analytics_insights_active(self, loc) -> bool:
        """Критерий 1: подпункт Инсайты стал активным (router-link-active)"""
        return self.page.locator(loc.ANALYTICS_INSIGHTS_ACTIVE).is_visible()

    def is_analytics_insights_page_open(self, loc) -> bool:
        """Критерий 2: открылась страница Аналитика > Инсайты"""
        return self.page.locator(loc.ANALYTICS_INSIGHTS_PAGE_HEADER).is_visible()

    def click_analytics_submenu_comparison(self, loc):
        """Кликает на подпункт подменю 'Сравнение' в разделе Аналитика"""
        self.click_on_elem(loc.ANALYTICS_SUBMENU_COMPARISON)

    def is_analytics_comparison_active(self, loc) -> bool:
        """Критерий 1: подпункт Сравнение стал активным (router-link-active)"""
        return self.page.locator(loc.ANALYTICS_COMPARISON_ACTIVE).is_visible()

    def is_analytics_comparison_page_open(self, loc) -> bool:
        """Критерий 2: открылась страница Аналитика > Сравнение"""
        return self.page.locator(loc.ANALYTICS_COMPARISON_PAGE_HEADER).is_visible()

    def click_menu_item_settings(self, loc):
        """Кликает на пункт меню 'Настройки'"""
        self.click_on_elem(loc.MENU_ITEM_SETTINGS)

    def is_settings_page_open(self, loc) -> bool:
        """Проверяет открытие страницы Настройки по наличию заголовка"""
        return self.page.locator(loc.SETTINGS_PAGE_TITLE).is_visible()

    def hover_help_menu(self, loc):
        """Ховер на элемент 'Нужна помощь?' для вызова ховер-меню"""
        self.hover_on_elem(loc.HELP_MENU_TRIGGER)

    def click_instructions(self, loc):
        """Кликает на кнопку 'Смотреть инструкции' в ховер-меню"""
        self.click_on_elem(loc.HELP_INSTRUCTIONS_BTN)

    def click_support(self, loc):
        """Кликает на кнопку 'Написать в поддержку' в ховер-меню"""
        self.click_on_elem(loc.HELP_SUPPORT_BTN)

    def hover_profile_menu(self, loc):
        """Ховер на блок профиля в футере сайдбара"""
        self.hover_on_elem(loc.PROFILE_MENU_TRIGGER)

    def click_my_profile(self, loc):
        """Кликает на кнопку 'Мой профиль' в ховер-меню профиля"""
        self.click_on_elem(loc.PROFILE_MY_PROFILE_BTN)

    def click_company(self, loc):
        """Кликает на кнопку 'Компания' в ховер-меню профиля"""
        self.click_on_elem(loc.PROFILE_COMPANY_BTN)

    def click_history(self, loc):
        """Кликает на кнопку 'История обработки' в ховер-меню профиля"""
        self.click_on_elem(loc.PROFILE_HISTORY_BTN)

    def click_logout(self, loc):
        """Кликает на кнопку 'Выход' в ховер-меню профиля"""
        self.click_on_elem(loc.PROFILE_LOGOUT_BTN)

    def click_confirm_logout(self, loc):
        """Кликает 'Да' в модальном окне подтверждения выхода"""
        self.click_on_elem(loc.LOGOUT_CONFIRM_YES_BTN)

    def get_current_url(self):
        """Возвращает текущий URL страницы"""
        return self.page.url

    def wait_for_new_tab_and_get_url(self, loc):
        """Ховер + клик с перехватом новой вкладки, возвращает URL новой вкладки.

        Если ссылка открывается в той же вкладке (нет target="_blank"),
        возвращает URL текущей страницы после навигации.
        """
        try:
            with self.page.context.expect_page(timeout=8000) as new_page_info:
                self.click_on_elem(loc.HELP_INSTRUCTIONS_BTN)
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

    # ── Узкое меню (narrow) ───────────────────────────────────────────────

    def collapse_sidebar(self, loc):
        """Сворачивает боковое меню до узкого, если оно широкое"""
        if not self.is_sidebar_collapsed(loc):
            self.click_on_elem(loc.SIDEBAR_BURGER)

    # Триггеры попапов — клик
    def click_menu_item_reviews_narrow(self, loc):
        """Кликает на иконку 'Отзывы' в узком меню для открытия попапа"""
        self.click_on_elem(loc.MENU_ITEM_REVIEWS_NARROW)

    def click_menu_item_analytics_narrow(self, loc):
        """Кликает на иконку 'Аналитика' в узком меню для открытия попапа"""
        self.click_on_elem(loc.MENU_ITEM_ANALYTICS_NARROW)

    # Триггеры попапов — ховер
    def hover_menu_item_reviews_narrow(self, loc):
        """Ховер на иконку 'Отзывы' в узком меню для открытия попапа"""
        self.hover_on_elem(loc.MENU_ITEM_REVIEWS_NARROW)

    def hover_menu_item_analytics_narrow(self, loc):
        """Ховер на иконку 'Аналитика' в узком меню для открытия попапа"""
        self.hover_on_elem(loc.MENU_ITEM_ANALYTICS_NARROW)

    # Прямые переходы — иконки без попапа
    def click_menu_item_chats_narrow(self, loc):
        """Кликает на иконку 'Чаты' в узком меню"""
        self.click_on_elem(loc.MENU_ITEM_CHATS_NARROW)

    def click_menu_item_products_narrow(self, loc):
        """Кликает на иконку 'Товары' в узком меню"""
        self.click_on_elem(loc.MENU_ITEM_PRODUCTS_NARROW)

    def click_menu_item_places_narrow(self, loc):
        """Кликает на иконку 'Места' в узком меню"""
        self.click_on_elem(loc.MENU_ITEM_PLACES_NARROW)

    def click_menu_item_clients_narrow(self, loc):
        """Кликает на иконку 'Клиенты' в узком меню"""
        self.click_on_elem(loc.MENU_ITEM_CLIENTS_NARROW)

    def click_menu_item_settings_narrow(self, loc):
        """Кликает на иконку 'Настройки' в узком меню"""
        self.click_on_elem(loc.MENU_ITEM_SETTINGS_NARROW)

    def is_narrow_popup_open(self, loc) -> bool:
        """Проверяет, что попап узкого меню открыт (.tooltip-menu)"""
        return self.page.locator(loc.NARROW_POPUP).is_visible()

    # Клик для открытия попапов «Помощь» и «Профиль» (узкое меню)
    def click_help_menu(self, loc):
        """Кликает на 'Нужна помощь?' для открытия попапа"""
        self.click_on_elem(loc.HELP_MENU_TRIGGER)

    def click_profile_menu(self, loc):
        """Кликает на блок профиля для открытия попапа"""
        self.click_on_elem(loc.PROFILE_MENU_TRIGGER)
