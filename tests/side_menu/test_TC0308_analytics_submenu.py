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
class TestTC0308AnalyticsSubmenu:

    @allure.title("TC-0308s: Раскрытие подменю Аналитика. Широкое меню")
    @allure.description(
        "Пререквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\\n"
        "Действие: клик на пункт меню 'Аналитика'.\\n"
        "Критерий успеха: "
        "наличие подпункта 'Отзывы' (class=item__link-text is-inactive)."
    )
    def test_TC0308_analytics_submenu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Аналитика'"):
            side_menu.click_menu_item_analytics(menu_locator)

        with allure.step("Проверить критерий: появился подпункт 'Отзывы' в подменю Аналитика"):
            side_menu.wait_locator(menu_locator.ANALYTICS_SUBMENU_REVIEWS)
            assert side_menu.is_analytics_submenu_open(menu_locator), \
                "Подменю Аналитика не раскрылось (подпункт 'Отзывы' с классом is-inactive не найден)"
