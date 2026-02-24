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
class TestTC0310AnalyticsProcessing:

    @allure.title("TC-0310s: Переход на страницу Аналитика|Обработка. Широкое меню")
    @allure.description(
        "Пререквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Обработка'.\\n"
        "Критерий 1: подпункт 'Обработка' активен (router-link-active router-link-exact-active item__link-text).\\n"
        "Критерий 2: открыта страница Аналитика > Обработка (analytics-section__header с текстом 'Обработка')."
    )
    def test_TC0310_analytics_processing(self, subadmin_page):
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
            side_menu.wait_locator(menu_locator.ANALYTICS_SUBMENU_PROCESSING)

        with allure.step("Кликнуть на подпункт подменю 'Обработка'"):
            side_menu.click_analytics_submenu_processing(menu_locator)

        with allure.step("Проверить критерий 1: подпункт 'Обработка' активен (router-link-active)"):
            side_menu.wait_locator(menu_locator.ANALYTICS_PROCESSING_ACTIVE)
            assert side_menu.is_analytics_processing_active(menu_locator), \
                "Подпункт 'Обработка' не стал активным (router-link-active не найден)"

        with allure.step("Проверить критерий 2: открылась страница Аналитика > Обработка"):
            side_menu.wait_locator(menu_locator.ANALYTICS_PROCESSING_PAGE_HEADER)
            assert side_menu.is_analytics_processing_page_open(menu_locator), \
                "Страница Аналитика > Обработка не открылась (analytics-section__header не найден)"
