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
class TestTC0302SubMenuReviews:

    @allure.title("TC-0302s: Раскрытие подменю Отзывы. Широкое меню")
    @allure.description(
        "Доступно для клиентов с маркетплейсами и картами.\n"
        "Пререквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент', "
        "боковое меню открыто (sidebar with-sidebar).\n"
        "Критерий успеха: подменю 'Отзывы' стало активным."
    )
    def test_TC0302_submenu_reviews_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Проверить пререквизит: боковое меню открыто (sidebar with-sidebar)"):
            assert side_menu.is_sidebar_open(menu_locator), \
                "Пререквизит не выполнен: боковое меню не открыто"

        with allure.step("Раскрыть пункт меню 'Отзывы' (item__link-text)"):
            side_menu.click_menu_item_reviews(menu_locator)

        with allure.step("Проверить, что подменю 'Отзывы' стало активным"):
            assert side_menu.is_submenu_active(menu_locator), \
                "Подменю 'Отзывы' не стало активным (router-link-active router-link-exact-active item__link-text)"
