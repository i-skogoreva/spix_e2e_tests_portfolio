import allure

from locators.client_filter_locators import ClientFilterLocators
from locators.side_menu_locators import SideMenuLocators
from pages.reviews_page import ReviewsPage
from pages.side_menu_page import SideMenuPage
from data.dataclasses.user_dataclass import UserData
from utils.assertions.assertions import Assertions

data = UserData()
client_locator = ClientFilterLocators()
menu_locator = SideMenuLocators()
assertion = Assertions()


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Смена клиента")
class TestTS03ClientManagement:

    @allure.title("TC-0301s: Смена клиента")
    @allure.description(
        "Пририквизит: субадмин авторизован на сайте.\n"
        "Переход в клиента с именем 'Лайковый клиент'.\n"
        "Критерий: перезагрузка страницы и отображение клиента в селекте."
    )
    def test_TC0301_change_client(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step(f"Найти header-client-filter__clients и выбрать клиента '{data.CLIENT_LAYKOVY}'"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)

        with allure.step("Проверить появление лоадера при смене клиента"):
            reviews_page.wait_loader_visible(client_locator)

        with allure.step("Дождаться исчезновения лоадера (страница отзывов перезагружена)"):
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step(f"Проверить, что клиент '{data.CLIENT_LAYKOVY}' отображается в селекте"):
            selected_client = reviews_page.get_selected_client(client_locator)
            assertion.assert_text(selected_client, data.CLIENT_LAYKOVY)


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0302SubMenuReviews:

    @allure.title("TC-0302s: Раскрытие подменю Отзывы. Широкое меню")
    @allure.description(
        "Доступно для клиентов с маркетплейсами и картами.\n"
        "Пририквизиты: субадмин авторизован на сайте, "
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

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Раскрыть пункт меню 'Отзывы' (item__link-text)"):
            side_menu.click_menu_item_reviews(menu_locator)

        with allure.step("Проверить, что подменю 'Отзывы' стало активным"):
            assertion.assert_true(
                side_menu.is_submenu_active(menu_locator),
                "Подменю 'Отзывы' не стало активным (router-link-active router-link-exact-active item__link-text)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0303ReviewsKarty:

    @allure.title("TC-0303s: Переход в отзывы Карт. Широкое меню")
    @allure.description(
        "Доступно для клиентов с маркетплейсами и картами.\n"
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент', "
        "боковое меню открыто (sidebar with-sidebar), "
        "пункт меню 'Отзывы' (item__link-text) открыт.\n"
        "Критерий успеха: aria-current='page' с текстом 'Карты'."
    )
    def test_TC0303_reviews_karty_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Открыть пункт меню 'Отзывы' (item__link-text)"):
            side_menu.click_menu_item_reviews(menu_locator)
            side_menu.wait_locator(menu_locator.SUBMENU_ACTIVE)

        with allure.step("Выбрать пункт подменю 'Карты' (item__link-text)"):
            side_menu.setup_skeleton_observer(menu_locator)
            side_menu.click_submenu_item_karty(menu_locator)

        with allure.step("Проверить критерий: пункт 'Карты' активен (aria-current='page')"):
            assertion.assert_true(
                side_menu.is_karty_aria_current(menu_locator),
                "Пункт 'Карты' не стал активным (aria-current='page' не найден)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0304ChatsPage:

    @allure.title("TC-0304s: Переход на страницу Чаты. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Чаты'.\n"
        "Критерий успеха: открытие страницы чатов (chat-list__search-wrapper-title)."
    )
    def test_TC0304_chats_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Чаты'"):
            side_menu.click_menu_item_chats(menu_locator)

        with allure.step("Проверить критерий: открылась страница чатов (chat-list__search-wrapper-title)"):
            side_menu.wait_locator(menu_locator.CHAT_PAGE_TITLE)
            assertion.assert_true(
                side_menu.is_chat_page_open(menu_locator),
                "Страница чатов не открылась (chat-list__search-wrapper-title не найден)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0305ProductsPage:

    @allure.title("TC-0305s: Переход на страницу Товары. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Товары'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Товары' (class=header__title)."
    )
    def test_TC0305_products_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Товары'"):
            side_menu.click_menu_item_products(menu_locator)

        with allure.step("Проверить критерий: открылась страница Товары (class=header__title с текстом 'Товары')"):
            side_menu.wait_locator(menu_locator.PRODUCTS_PAGE_TITLE)
            assertion.assert_true(
                side_menu.is_products_page_open(menu_locator),
                "Страница Товары не открылась (class=header__title с текстом 'Товары' не найден)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0306PlacesPage:

    @allure.title("TC-0306s: Переход на страницу Места. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Места'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Места' (class=header__title)."
    )
    def test_TC0306_places_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Места'"):
            side_menu.click_menu_item_places(menu_locator)

        with allure.step("Проверить критерий: открылась страница Места (class=header__title с текстом 'Места')"):
            side_menu.wait_locator(menu_locator.PLACES_PAGE_TITLE)
            assertion.assert_true(
                side_menu.is_places_page_open(menu_locator),
                "Страница Места не открылась (class=header__title с текстом 'Места' не найден)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0307ClientsPage:

    @allure.title("TC-0307s: Переход на страницу Клиенты. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Клиенты'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Клиенты' (class=header__title)."
    )
    def test_TC0307_clients_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Клиенты'"):
            side_menu.click_menu_item_clients(menu_locator)

        with allure.step("Проверить критерий: открылась страница Клиенты (class=header__title с текстом 'Клиенты')"):
            side_menu.wait_locator(menu_locator.CLIENTS_PAGE_TITLE)
            assertion.assert_true(
                side_menu.is_clients_page_open(menu_locator),
                "Страница Клиенты не открылась (class=header__title с текстом 'Клиенты' не найден)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0308AnalyticsSubmenu:

    @allure.title("TC-0308s: Раскрытие подменю Аналитика. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика'.\n"
        "Критерий успеха: наличие подпункта 'Отзывы' (class=item__link-text is-inactive)."
    )
    def test_TC0308_analytics_submenu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Аналитика'"):
            side_menu.click_menu_item_analytics(menu_locator)

        with allure.step("Проверить критерий: появился подпункт 'Отзывы' в подменю Аналитика"):
            side_menu.wait_locator(menu_locator.ANALYTICS_SUBMENU_REVIEWS)
            assertion.assert_true(
                side_menu.is_analytics_submenu_open(menu_locator),
                "Подменю Аналитика не раскрылось (подпункт 'Отзывы' с классом is-inactive не найден)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0309AnalyticsReviews:

    @allure.title("TC-0309s: Переход на страницу Аналитика|Отзывы. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Отзывы'.\n"
        "Критерий успеха: открыта страница Аналитика > Отзывы (analytics-section__header с текстом 'Отзывы')."
    )
    def test_TC0309_analytics_reviews(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(menu_locator)
            side_menu.wait_locator(menu_locator.ANALYTICS_SUBMENU_REVIEWS)

        with allure.step("Кликнуть на подпункт подменю 'Отзывы'"):
            side_menu.click_analytics_submenu_reviews(menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Отзывы"):
            side_menu.wait_locator(menu_locator.ANALYTICS_REVIEWS_PAGE_HEADER)
            assertion.assert_true(
                side_menu.is_analytics_reviews_page_open(menu_locator),
                "Страница Аналитика > Отзывы не открылась (analytics-section__header не найден)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0310AnalyticsProcessing:

    @allure.title("TC-0310s: Переход на страницу Аналитика|Обработка. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Обработка'.\n"
        "Критерий успеха: открыта страница Аналитика > Обработка (analytics-section__header с текстом 'Обработка')."
    )
    def test_TC0310_analytics_processing(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(menu_locator)
            side_menu.wait_locator(menu_locator.ANALYTICS_SUBMENU_PROCESSING)

        with allure.step("Кликнуть на подпункт подменю 'Обработка'"):
            side_menu.click_analytics_submenu_processing(menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Обработка"):
            side_menu.wait_locator(menu_locator.ANALYTICS_PROCESSING_PAGE_HEADER)
            assertion.assert_true(
                side_menu.is_analytics_processing_page_open(menu_locator),
                "Страница Аналитика > Обработка не открылась (analytics-section__header не найден)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0311AnalyticsInsights:

    @allure.title("TC-0311s: Переход на страницу Аналитика|Инсайты. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Инсайты'.\n"
        "Критерий успеха: открыта страница Аналитика > Инсайты (analytics-section__header с текстом 'Инсайты')."
    )
    def test_TC0311_analytics_insights(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(menu_locator)
            side_menu.wait_locator(menu_locator.ANALYTICS_SUBMENU_INSIGHTS)

        with allure.step("Кликнуть на подпункт подменю 'Инсайты'"):
            side_menu.click_analytics_submenu_insights(menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Инсайты"):
            side_menu.wait_locator(menu_locator.ANALYTICS_INSIGHTS_PAGE_HEADER)
            assertion.assert_true(
                side_menu.is_analytics_insights_page_open(menu_locator),
                "Страница Аналитика > Инсайты не открылась (analytics-section__header не найден)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0312AnalyticsComparison:

    @allure.title("TC-0312s: Переход на страницу Аналитика|Сравнение. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Сравнение'.\n"
        "Критерий успеха: открыта страница Аналитика > Сравнение (analytics-section__header с текстом 'Сравнение')."
    )
    def test_TC0312_analytics_comparison(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(menu_locator)
            side_menu.wait_locator(menu_locator.ANALYTICS_SUBMENU_COMPARISON)

        with allure.step("Кликнуть на подпункт подменю 'Сравнение'"):
            side_menu.click_analytics_submenu_comparison(menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Сравнение"):
            side_menu.wait_locator(menu_locator.ANALYTICS_COMPARISON_PAGE_HEADER)
            assertion.assert_true(
                side_menu.is_analytics_comparison_page_open(menu_locator),
                "Страница Аналитика > Сравнение не открылась (analytics-section__header не найден)"
            )


@allure.parent_suite("side_menu")
@allure.suite("TS-03 Боковое меню")
class TestTC0313SettingsPage:

    @allure.title("TC-0313s: Переход на страницу Настройки. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Настройки'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Настройки' (class=header__title)."
    )
    def test_TC0313_settings_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(menu_locator)

        with allure.step(f"Выбрать клиента '{data.CLIENT_LAYKOVY}' в header-client-filter__clients"):
            reviews_page.select_client(client_locator, data.CLIENT_LAYKOVY)
            reviews_page.wait_loader_visible(client_locator)
            reviews_page.wait_loader_hidden(client_locator)

        with allure.step("Кликнуть на пункт меню 'Настройки'"):
            side_menu.click_menu_item_settings(menu_locator)

        with allure.step("Проверить критерий: открылась страница Настройки (class=header__title с текстом 'Настройки')"):
            side_menu.wait_locator(menu_locator.SETTINGS_PAGE_TITLE)
            assertion.assert_true(
                side_menu.is_settings_page_open(menu_locator),
                "Страница Настройки не открылась (class=header__title с текстом 'Настройки' не найден)"
            )
