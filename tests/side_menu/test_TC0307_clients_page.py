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
class TestTC0307ClientsPage:

    @allure.title("TC-0307s: Переход на страницу Клиенты. Широкое меню")
    @allure.description(
        "Пререквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\\n"
        "Действие: клик на пункт меню 'Клиенты'.\\n"
        "Критерий успеха: "
        "открытие страницы с заголовком 'Клиенты' (class=header__title)."
    )
    def test_TC0307_clients_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Клиенты'"):
            side_menu.click_menu_item_clients(menu_locator)

        with allure.step("Проверить критерий: открылась страница Клиенты (class=header__title с текстом 'Клиенты')"):
            side_menu.wait_locator(menu_locator.CLIENTS_PAGE_TITLE)
            assert side_menu.is_clients_page_open(menu_locator), \
                "Страница Клиенты не открылась (class=header__title с текстом 'Клиенты' не найден)"
