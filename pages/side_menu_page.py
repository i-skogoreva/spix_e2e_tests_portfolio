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
