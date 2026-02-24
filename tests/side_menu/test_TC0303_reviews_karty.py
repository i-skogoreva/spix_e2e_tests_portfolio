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
class TestTC0303ReviewsKarty:

    @allure.title("TC-0303s: Переход в отзывы Карт. Широкое меню")
    @allure.description(
        "Доступно для клиентов с маркетплейсами и картами.\n"
        "Пререквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент', "
        "боковое меню открыто (sidebar with-sidebar), "
        "пункт меню 'Отзывы' (item__link-text) открыт.\n"
        "Критерии успеха: "
        "1. aria-current='page' с текстом 'Карты'. "
        "2. Появление скелетона (v-overlay-container)."
    )
    def test_TC0303_reviews_karty_wide_menu(self, subadmin_page):
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

        with allure.step("Открыть пункт меню 'Отзывы' (item__link-text)"):
            side_menu.click_menu_item_reviews(menu_locator)
            side_menu.wait_locator(menu_locator.SUBMENU_ACTIVE)

        with allure.step("Выбрать пункт подменю 'Карты' (item__link-text)"):
            side_menu.setup_skeleton_observer(menu_locator)
            side_menu.click_submenu_item_karty(menu_locator)

        with allure.step("Проверить критерий 1: пункт 'Карты' активен (aria-current='page')"):
            assert side_menu.is_karty_aria_current(menu_locator), \
                "Пункт 'Карты' не стал активным (aria-current='page' не найден)"

        with allure.step("Проверить критерий 2: появление скелетона (loader-wrapper)"):
            side_menu.check_skeleton_appeared()
