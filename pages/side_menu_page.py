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
