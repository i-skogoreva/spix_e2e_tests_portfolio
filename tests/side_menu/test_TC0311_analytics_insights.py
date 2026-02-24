import allure

from locators.client_filter_locators import ClientFilterLocators
from locators.side_menu_locators import SideMenuLocators
from pages.reviews_page import ReviewsPage
from pages.side_menu_page import SideMenuPage
from data.dataclasses.user_dataclass import UserData

data = UserData()
client_locator = ClientFilterLocators()
menu_locator = SideMenuLocators()


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0311AnalyticsInsights:

    @allure.title("TC-0311s: Переход на страницу Аналитика|Инсайты. Широкое меню")
    @allure.description(
        "Пререквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Инсайты'.\\n"
        "Критерий 1: подпункт 'Инсайты' активен (router-link-active router-link-exact-active item__link-text).\\n"
        "Критерий 2: открыта страница Аналитика > Инсайты (analytics-section__header с текстом 'Инсайты')."
    )
    def test_TC0311_analytics_insights(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(menu_locator)
            side_menu.wait_locator(menu_locator.ANALYTICS_SUBMENU_INSIGHTS)

        with allure.step("Кликнуть на подпункт подменю 'Инсайты'"):
            side_menu.click_analytics_submenu_insights(menu_locator)

        with allure.step("Проверить критерий 1: подпункт 'Инсайты' активен (router-link-active)"):
            side_menu.wait_locator(menu_locator.ANALYTICS_INSIGHTS_ACTIVE)
            assert side_menu.is_analytics_insights_active(menu_locator), \
                "Подпункт 'Инсайты' не стал активным (router-link-active не найден)"

        with allure.step("Проверить критерий 2: открылась страница Аналитика > Инсайты"):
            side_menu.wait_locator(menu_locator.ANALYTICS_INSIGHTS_PAGE_HEADER)
            assert side_menu.is_analytics_insights_page_open(menu_locator), \
                "Страница Аналитика > Инсайты не открылась (analytics-section__header не найден)"
