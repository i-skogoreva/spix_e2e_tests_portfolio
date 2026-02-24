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
class TestTC0304ChatsPage:

    @allure.title("TC-0304s: Переход на страницу Чаты. Широкое меню")
    @allure.description(
        "Пререквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Чаты'.\n"
        "Критерии успеха: "
        "1. Открытие страницы чатов (chat-list__search-wrapper-title). "
        "2. Схлопывание бокового меню (sidebar без with-sidebar)."
    )
    def test_TC0304_chats_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Чаты'"):
            side_menu.click_menu_item_chats(menu_locator)

        with allure.step("Проверить критерий 1: открылась страница чатов (chat-list__search-wrapper-title)"):
            side_menu.wait_locator(menu_locator.CHAT_PAGE_TITLE)
            assert side_menu.is_chat_page_open(menu_locator), \
                "Страница чатов не открылась (chat-list__search-wrapper-title не найден)"

        with allure.step("Проверить критерий 2: боковое меню схлопнулось (sidebar без with-sidebar)"):
            assert side_menu.is_sidebar_collapsed(menu_locator), \
                "Боковое меню не схлопнулось (класс with-sidebar всё ещё присутствует)"
