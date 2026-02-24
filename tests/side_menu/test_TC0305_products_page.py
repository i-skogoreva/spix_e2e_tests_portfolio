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
class TestTC0305ProductsPage:

    @allure.title("TC-0305s: Переход на страницу Товары. Широкое меню")
    @allure.description(
        "Пререквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\\n"
        "Действие: клик на пункт меню 'Товары'.\\n"
        "Критерий успеха: "
        "открытие страницы с заголовком 'Товары' (h1)."
    )
    def test_TC0305_products_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Товары'"):
            side_menu.click_menu_item_products(menu_locator)

        with allure.step("Проверить критерий: открылась страница Товары (h1 с текстом 'Товары')"):
            side_menu.wait_locator(menu_locator.PRODUCTS_PAGE_TITLE)
            assert side_menu.is_products_page_open(menu_locator), \
                "Страница Товары не открылась (h1 с текстом 'Товары' не найден)"
