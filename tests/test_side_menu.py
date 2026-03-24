import allure

from locators.client_filter_locators import ClientFilterLocators
from locators.clients_page_locators import ClientsPageLocators
from locators.side_menu_locators import SideMenuLocators
from locators.operator_locators import OperatorLocators
from pages.clients_page import ClientsPage
from pages.reviews_page import ReviewsPage
from pages.side_menu_page import SideMenuPage
from pages.operator_page import OperatorPage
from data.dataclasses.user_dataclass import UserData
from data.endpoints import Endpoints
from utils.assertions.assertions import Assertions


@allure.feature("side_menu")
@allure.story("TS-03 Боковое меню")
class TestTS03SideMenu:
    data = UserData()
    endpoints = Endpoints()
    client_locator = ClientFilterLocators()
    menu_locator = SideMenuLocators()
    assertion = Assertions()

    @allure.title("TC-0302s"
                  ": Раскрытие подменю Отзывы. Широкое меню")
    @allure.description(
        "Доступно для клиентов с маркетплейсами и картами.\n"
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент', "
        "боковое меню открыто (sidebar with-sidebar).\n"
        "Критерий успеха: подменю 'Отзывы' стало активным."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0302_submenu_reviews_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Раскрыть пункт меню 'Отзывы' (item__link-text)"):
            side_menu.click_menu_item_reviews(self.menu_locator)

        with allure.step("Проверить, что подменю 'Отзывы' стало активным"):
            self.assertion.assert_true(
                side_menu.is_submenu_active(self.menu_locator),
                "Подменю 'Отзывы' не стало активным (router-link-active router-link-exact-active item__link-text)"
            )

    @allure.title("TC-0303s: Переход в отзывы Карт. Широкое меню")
    @allure.description(
        "Доступно для клиентов с маркетплейсами и картами.\n"
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент', "
        "боковое меню открыто (sidebar with-sidebar), "
        "пункт меню 'Отзывы' (item__link-text) открыт.\n"
        "Критерий успеха: aria-current='page' с текстом 'Карты'."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0303_reviews_karty_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Открыть пункт меню 'Отзывы' (item__link-text)"):
            side_menu.click_menu_item_reviews(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SUBMENU_ACTIVE)

        with allure.step("Выбрать пункт подменю 'Карты' (item__link-text)"):
            side_menu.setup_skeleton_observer(self.menu_locator)
            side_menu.click_submenu_item_karty(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Карты (URL содержит /home-pois)"):
            side_menu.wait_url_contains(self.endpoints.HOME_POIS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.HOME_POIS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.HOME_POIS_ENDPOINT}"
            )

    @allure.title("TC-0304s: Переход на страницу Чаты. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Чаты'.\n"
        "Критерий успеха: открытие страницы чатов (chat-list__search-wrapper-title)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0304_chats_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Чаты'"):
            side_menu.click_menu_item_chats(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница чатов (URL содержит /chats)"):
            side_menu.wait_url_contains(self.endpoints.CHATS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.CHATS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.CHATS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0305s: Переход на страницу Товары. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Товары'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Товары' (class=header__title)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0305_products_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Товары'"):
            side_menu.click_menu_item_products(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Товары (URL содержит /products)"):
            side_menu.wait_url_contains(self.endpoints.PRODUCTS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PRODUCTS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.PRODUCTS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0306s: Переход на страницу Места. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Места'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Места' (class=header__title)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0306_places_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Места'"):
            side_menu.click_menu_item_places(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Места (URL содержит /pois)"):
            side_menu.wait_url_contains(self.endpoints.POIS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.POIS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.POIS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0307s: Переход на страницу Клиенты. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Клиенты'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Клиенты' (class=header__title)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0307_clients_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Клиенты'"):
            side_menu.click_menu_item_clients(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Клиенты (URL содержит /clients)"):
            side_menu.wait_url_contains(self.endpoints.CLIENTS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.CLIENTS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.CLIENTS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0308s: Раскрытие подменю Аналитика. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика'.\n"
        "Критерий успеха: наличие подпункта 'Отзывы' (class=item__link-text is-inactive)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0308_analytics_submenu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Аналитика'"):
            side_menu.click_menu_item_analytics(self.menu_locator)

        with allure.step("Проверить критерий: появился подпункт 'Отзывы' в подменю Аналитика"):
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_REVIEWS)
            self.assertion.assert_true(
                side_menu.is_analytics_submenu_open(self.menu_locator),
                "Подменю Аналитика не раскрылось (подпункт 'Отзывы' с классом is-inactive не найден)"
            )

    @allure.title("TC-0309s: Переход на страницу Аналитика|Отзывы. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Отзывы'.\n"
        "Критерий успеха: открыта страница Аналитика > Отзывы (analytics-section__header с текстом 'Отзывы')."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0309_analytics_reviews(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_REVIEWS)

        with allure.step("Кликнуть на подпункт подменю 'Отзывы'"):
            side_menu.click_analytics_submenu_reviews(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Отзывы (URL содержит /review-analytics)"):
            side_menu.wait_url_contains(self.endpoints.REVIEW_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.REVIEW_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.REVIEW_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0310s: Переход на страницу Аналитика|Обработка. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Обработка'.\n"
        "Критерий успеха: открыта страница Аналитика > Обработка (analytics-section__header с текстом 'Обработка')."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0310_analytics_processing(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_PROCESSING)

        with allure.step("Кликнуть на подпункт подменю 'Обработка'"):
            side_menu.click_analytics_submenu_processing(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Обработка (URL содержит /processing-analytics)"):
            side_menu.wait_url_contains(self.endpoints.PROCESSING_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PROCESSING_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.PROCESSING_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0311s: Переход на страницу Аналитика|Инсайты. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Инсайты'.\n"
        "Критерий успеха: открыта страница Аналитика > Инсайты (analytics-section__header с текстом 'Инсайты')."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0311_analytics_insights(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_INSIGHTS)

        with allure.step("Кликнуть на подпункт подменю 'Инсайты'"):
            side_menu.click_analytics_submenu_insights(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Инсайты (URL содержит /insights)"):
            side_menu.wait_url_contains(self.endpoints.INSIGHTS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.INSIGHTS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.INSIGHTS_ENDPOINT}"
            )

    @allure.title("TC-0312s: Переход на страницу Аналитика|Сравнение. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Сравнение'.\n"
        "Критерий успеха: открыта страница Аналитика > Сравнение (analytics-section__header с текстом 'Сравнение')."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0312_analytics_comparison(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_COMPARISON)

        with allure.step("Кликнуть на подпункт подменю 'Сравнение'"):
            side_menu.click_analytics_submenu_comparison(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Сравнение (URL содержит /comparison-analytics)"):
            side_menu.wait_url_contains(self.endpoints.COMPARISON_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.COMPARISON_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.COMPARISON_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0313s: Переход на страницу Настройки. Широкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Настройки'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Настройки' (class=header__title)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0313_settings_page_wide_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Настройки'"):
            side_menu.click_menu_item_settings(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Настройки (URL содержит /settings)"):
            side_menu.wait_url_contains(self.endpoints.SETTINGS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.SETTINGS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.SETTINGS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0314s: Переход в инструкции через ховер-меню 'Нужна помощь?'")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: ховер на 'Нужна помощь?' → клик 'Смотреть инструкции'.\n"
        "Критерий успеха: открылась новая вкладка с URL https://spix.ru/instructions/."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0314_instructions_hover_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Ховер на элемент 'Нужна помощь?' в сайдбаре"):
            side_menu.hover_help_menu(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.HELP_INSTRUCTIONS_BTN)

        with allure.step("Кликнуть 'Смотреть инструкции' и проверить новую вкладку"):
            new_tab_url = side_menu.wait_for_new_tab_and_get_url(self.menu_locator)
            self.assertion.assert_url(new_tab_url, self.endpoints.INSTRUCTIONS_URL)

    @allure.title("TC-0315s: Переход в техподдержку через ховер-меню 'Нужна помощь?'")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: ховер на 'Нужна помощь?' → клик 'Написать в поддержку'.\n"
        "Критерий успеха: переход на страницу /support."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0315_support_hover_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Ховер на элемент 'Нужна помощь?' в сайдбаре"):
            side_menu.hover_help_menu(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.HELP_SUPPORT_BTN)

        with allure.step("Кликнуть 'Написать в поддержку' и проверить URL"):
            side_menu.click_support(self.menu_locator)
            side_menu.wait_url(f"**{self.endpoints.SUPPORT_PAGE_ENDPOINT}")
            self.assertion.assert_true(
                self.endpoints.SUPPORT_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.SUPPORT_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0316s: Переход в профиль через ховер-меню профиля")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: ховер на профиль → клик 'Мой профиль'.\n"
        "Критерий успеха: переход на страницу /profile."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0316_profile_hover_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Ховер на блок профиля в футере сайдбара"):
            side_menu.hover_profile_menu(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.PROFILE_MY_PROFILE_BTN)

        with allure.step("Кликнуть 'Мой профиль' и проверить URL"):
            side_menu.click_my_profile(self.menu_locator)
            side_menu.wait_url_contains(self.endpoints.PROFILE_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PROFILE_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.PROFILE_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0317s: Выход из ЛК через ховер-меню профиля")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: ховер на профиль → клик 'Выход' → подтверждение 'Да'.\n"
        "Критерий успеха: редирект на страницу авторизации /signin/."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0317_logout_hover_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Ховер на блок профиля в футере сайдбара"):
            side_menu.hover_profile_menu(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.PROFILE_LOGOUT_BTN)

        with allure.step("Кликнуть 'Выход' в ховер-меню"):
            side_menu.click_logout(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.LOGOUT_CONFIRM_YES_BTN)

        with allure.step("Подтвердить выход — кликнуть 'Да' и проверить редирект на /signin/"):
            side_menu.click_confirm_logout(self.menu_locator)
            side_menu.wait_url_contains(self.endpoints.AUTHORIZATION_USER_ENDPOINT.rstrip('/'))
            self.assertion.assert_true(
                self.endpoints.AUTHORIZATION_USER_ENDPOINT.rstrip('/') in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.AUTHORIZATION_USER_ENDPOINT}"
            )

    @allure.title("TC-0337s: Переход на страницу отзывов клиента со страницы Клиенты")
    @allure.description(
        "Предусловия: субадмин авторизован, тестовый клиент «Авто_тест» создан.\n"
        "Шаги: 1. Открыть страницу Клиенты. "
        "2. Кликнуть кнопку «Смотреть отзывы клиента» в строке «Авто_тест».\n"
        "Критерий успеха: URL содержит /1, feedbacks_tab=pending и client_id клиента."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0337_client_reviews_from_clients_page(self, subadmin_page, auto_client):
        clients_page = ClientsPage(
            subadmin_page,
            url=self.data.BASE_URL + self.endpoints.CLIENTS_PAGE_ENDPOINT
        )
        clients_locator = ClientsPageLocators()

        with allure.step("Открыть страницу Клиенты"):
            clients_page.open()
        with allure.step("Кликнуть кнопку «Смотреть отзывы клиента» в строке клиента"):
            clients_page.click_client_reviews(clients_locator, auto_client["nm"])
        with allure.step("Проверить URL"):
            clients_page.wait_url_contains("feedbacks_tab=pending")
            url = clients_page.get_current_url()
            self.assertion.assert_true(
                f"client_id={auto_client['id']}" in url and "feedbacks_tab=pending" in url,
                f"URL должен содержать client_id={auto_client['id']} и feedbacks_tab=pending"
            )

    @allure.title("TC-0338s: Переход на страницу товаров клиента со страницы Клиенты")
    @allure.description(
        "Предусловия: субадмин авторизован, тестовый клиент «Авто_тест» создан.\n"
        "Шаги: 1. Открыть страницу Клиенты. "
        "2. Кликнуть кнопку «Смотреть товары клиента» в строке «Авто_тест».\n"
        "Критерий успеха: URL содержит /products/1 и client_id клиента."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0338_client_products_from_clients_page(self, subadmin_page, auto_client):
        clients_page = ClientsPage(
            subadmin_page,
            url=self.data.BASE_URL + self.endpoints.CLIENTS_PAGE_ENDPOINT
        )
        clients_locator = ClientsPageLocators()

        with allure.step("Открыть страницу Клиенты"):
            clients_page.open()
        with allure.step("Кликнуть кнопку «Смотреть товары клиента» в строке клиента"):
            clients_page.click_client_products(clients_locator, auto_client["nm"])
        with allure.step("Проверить URL"):
            clients_page.wait_url_contains("/products/1")
            url = clients_page.get_current_url()
            self.assertion.assert_true(
                "/products/1" in url and f"client_id={auto_client['id']}" in url,
                f"URL должен содержать /products/1 и client_id={auto_client['id']}"
            )

    @allure.title("TC-0339s: Переход на страницу карт клиента со страницы Клиенты")
    @allure.description(
        "Предусловия: субадмин авторизован, тестовый клиент «Авто_тест» создан.\n"
        "Шаги: 1. Открыть страницу Клиенты. "
        "2. Кликнуть кнопку «Карты» в строке «Авто_тест».\n"
        "Критерий успеха: URL содержит /pois/1 и client_id клиента."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0339_client_maps_from_clients_page(self, subadmin_page, auto_client):
        clients_page = ClientsPage(
            subadmin_page,
            url=self.data.BASE_URL + self.endpoints.CLIENTS_PAGE_ENDPOINT
        )
        clients_locator = ClientsPageLocators()

        with allure.step("Открыть страницу Клиенты"):
            clients_page.open()
        with allure.step("Кликнуть кнопку «Карты» в строке клиента"):
            clients_page.click_client_maps(clients_locator, auto_client["nm"])
        with allure.step("Проверить URL"):
            clients_page.wait_url_contains("/pois/1")
            url = clients_page.get_current_url()
            self.assertion.assert_true(
                "/pois/1" in url and f"client_id={auto_client['id']}" in url,
                f"URL должен содержать /pois/1 и client_id={auto_client['id']}"
            )

    @allure.title("TC-0340s: Переход на страницу брендов клиента со страницы Клиенты")
    @allure.description(
        "Предусловия: субадмин авторизован, тестовый клиент «Авто_тест» создан.\n"
        "Шаги: 1. Открыть страницу Клиенты. "
        "2. Кликнуть кнопку «Смотреть бренды клиента» в строке «Авто_тест».\n"
        "Критерий успеха: URL содержит /brands/{client_id} (id клиента в пути)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0340_client_brands_from_clients_page(self, subadmin_page, auto_client):
        clients_page = ClientsPage(
            subadmin_page,
            url=self.data.BASE_URL + self.endpoints.CLIENTS_PAGE_ENDPOINT
        )
        clients_locator = ClientsPageLocators()

        with allure.step("Открыть страницу Клиенты"):
            clients_page.open()
        with allure.step("Кликнуть кнопку «Смотреть бренды клиента» в строке клиента"):
            clients_page.click_client_brands(clients_locator, auto_client["nm"])
        with allure.step("Проверить URL"):
            url = clients_page.get_current_url()
            self.assertion.assert_true(
                f"/brands/{auto_client['id']}" in url,
                f"URL должен содержать /brands/{auto_client['id']}"
            )

    @allure.title("TC-0341s: Переход в группу шаблонных ответов клиента со страницы Клиенты")
    @allure.description(
        "Предусловия: субадмин авторизован, тестовый клиент «Авто_тест» создан.\n"
        "Шаги: 1. Открыть страницу Клиенты. "
        "2. Кликнуть кнопку «Смотреть группы шаблонных ответов клиента» в строке «Авто_тест».\n"
        "Критерий успеха: URL содержит /settings/template-answers и client_id клиента."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0341_client_templates_from_clients_page(self, subadmin_page, auto_client):
        clients_page = ClientsPage(
            subadmin_page,
            url=self.data.BASE_URL + self.endpoints.CLIENTS_PAGE_ENDPOINT
        )
        clients_locator = ClientsPageLocators()

        with allure.step("Открыть страницу Клиенты"):
            clients_page.open()
        with allure.step("Кликнуть кнопку «Шаблонные ответы» в строке клиента"):
            clients_page.click_client_templates(clients_locator, auto_client["nm"])
        with allure.step("Проверить URL"):
            clients_page.wait_url_contains(self.endpoints.TEMPLATE_ANSWERS_ENDPOINT)
            url = clients_page.get_current_url()
            self.assertion.assert_true(
                self.endpoints.TEMPLATE_ANSWERS_ENDPOINT in url and f"client_id={auto_client['id']}" in url,
                f"URL должен содержать {self.endpoints.TEMPLATE_ANSWERS_ENDPOINT} и client_id={auto_client['id']}"
            )

    @allure.title("TC-0342s: Переход на страницу пользователей клиента со страницы Клиенты")
    @allure.description(
        "Предусловия: субадмин авторизован, тестовый клиент «Авто_тест» создан.\n"
        "Шаги: 1. Открыть страницу Клиенты. "
        "2. Кликнуть кнопку «Смотреть пользователей клиента» в строке «Авто_тест».\n"
        "Критерий успеха: URL содержит /settings-company/users и client_id клиента."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0342_client_users_from_clients_page(self, subadmin_page, auto_client):
        clients_page = ClientsPage(
            subadmin_page,
            url=self.data.BASE_URL + self.endpoints.CLIENTS_PAGE_ENDPOINT
        )
        clients_locator = ClientsPageLocators()

        with allure.step("Открыть страницу Клиенты"):
            clients_page.open()
        with allure.step("Кликнуть кнопку «Пользователи» в строке клиента"):
            clients_page.click_client_users(clients_locator, auto_client["nm"])
        with allure.step("Проверить URL"):
            clients_page.wait_url_contains(self.endpoints.SETTINGS_COMPANY_USERS_ENDPOINT)
            url = clients_page.get_current_url()
            self.assertion.assert_true(
                self.endpoints.SETTINGS_COMPANY_USERS_ENDPOINT in url and f"client_id={auto_client['id']}" in url,
                f"URL должен содержать {self.endpoints.SETTINGS_COMPANY_USERS_ENDPOINT} и client_id={auto_client['id']}"
            )

    @allure.title("TC-0343s: Переход в настройки компании клиента со страницы Клиенты")
    @allure.description(
        "Предусловия: субадмин авторизован, тестовый клиент «Авто_тест» создан.\n"
        "Шаги: 1. Открыть страницу Клиенты. "
        "2. Кликнуть кнопку «Настройки компании клиента» (gear) в строке «Авто_тест».\n"
        "Критерий успеха: URL содержит /settings-company/settings и client_id клиента."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0343_client_settings_from_clients_page(self, subadmin_page, auto_client):
        clients_page = ClientsPage(
            subadmin_page,
            url=self.data.BASE_URL + self.endpoints.CLIENTS_PAGE_ENDPOINT
        )
        clients_locator = ClientsPageLocators()

        with allure.step("Открыть страницу Клиенты"):
            clients_page.open()
        with allure.step("Кликнуть кнопку «Настройки компании» в строке клиента"):
            clients_page.click_client_settings(clients_locator, auto_client["nm"])
        with allure.step("Проверить URL"):
            url = clients_page.get_current_url()
            self.assertion.assert_true(
                self.endpoints.SETTINGS_COMPANY_ENDPOINT in url and f"client_id={auto_client['id']}" in url,
                f"URL должен содержать {self.endpoints.SETTINGS_COMPANY_ENDPOINT} и client_id={auto_client['id']}"
            )

    @allure.title("TC-0344s: Переход в финансы клиента со страницы Клиенты")
    @allure.description(
        "Предусловия: субадмин авторизован, тестовый клиент «Авто_тест» создан.\n"
        "Шаги: 1. Открыть страницу Клиенты. "
        "2. Кликнуть кнопку «Финансы» (card-иконка) в строке «Авто_тест».\n"
        "Критерий успеха: URL содержит /settings-company/billing и client_id клиента."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0344_client_billing_from_clients_page(self, subadmin_page, auto_client):
        clients_page = ClientsPage(
            subadmin_page,
            url=self.data.BASE_URL + self.endpoints.CLIENTS_PAGE_ENDPOINT
        )
        clients_locator = ClientsPageLocators()

        with allure.step("Открыть страницу Клиенты"):
            clients_page.open()
        with allure.step("Кликнуть кнопку «Финансы» в строке клиента"):
            clients_page.click_client_billing(clients_locator, auto_client["nm"])
        with allure.step("Проверить URL"):
            clients_page.wait_url_contains(self.endpoints.SETTINGS_COMPANY_BILLING_ENDPOINT)
            url = clients_page.get_current_url()
            self.assertion.assert_true(
                self.endpoints.SETTINGS_COMPANY_BILLING_ENDPOINT in url and f"client_id={auto_client['id']}" in url,
                f"URL должен содержать {self.endpoints.SETTINGS_COMPANY_BILLING_ENDPOINT} и client_id={auto_client['id']}"
            )


@allure.feature("side_menu")
@allure.story("TS-03 Боковое меню")
class TestTS03SideMenuNarrow:
    data = UserData()
    endpoints = Endpoints()
    client_locator = ClientFilterLocators()
    menu_locator = SideMenuLocators()
    assertion = Assertions()

    @allure.title("TC-0318s: Сворачивание бокового меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню широкое.\n"
        "Действие: клик на burger для сворачивания меню.\n"
        "Критерий успеха: боковое меню стало узким (.sidebar-wrapper.small)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0318_collapse_sidebar(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)

        with allure.step("Кликнуть burger для сворачивания бокового меню"):
            side_menu.click_on_elem(self.menu_locator.SIDEBAR_BURGER)

        with allure.step("Проверить критерий: боковое меню стало узким (.sidebar-wrapper.small)"):
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)
            self.assertion.assert_true(
                side_menu.is_sidebar_collapsed(self.menu_locator),
                "Боковое меню не свернулось (.sidebar-wrapper.small не найден)"
            )

    @allure.title("TC-0319s: Раскрытие попап 'Отзывы' кликом. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Отзывы'.\n"
        "Критерий успеха: появился попап-меню (.tooltip-menu)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0319_reviews_popup_click_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Отзывы' в узком меню"):
            side_menu.click_menu_item_reviews_narrow(self.menu_locator)

        with allure.step("Проверить критерий: попап-меню 'Отзывы' открылся (.tooltip-menu)"):
            side_menu.wait_locator(self.menu_locator.NARROW_POPUP)
            self.assertion.assert_true(
                side_menu.is_narrow_popup_open(self.menu_locator),
                "Попап-меню 'Отзывы' не открылся (.tooltip-menu не найден)"
            )

    @allure.title("TC-0320s: Раскрытие попап 'Отзывы' ховером. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: ховер на иконку 'Отзывы'.\n"
        "Критерий успеха: появился попап-меню (.tooltip-menu)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0320_reviews_popup_hover_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Ховер на иконку 'Отзывы' в узком меню"):
            side_menu.hover_menu_item_reviews_narrow(self.menu_locator)

        with allure.step("Проверить критерий: попап-меню 'Отзывы' открылся (.tooltip-menu)"):
            side_menu.wait_locator(self.menu_locator.NARROW_POPUP)
            self.assertion.assert_true(
                side_menu.is_narrow_popup_open(self.menu_locator),
                "Попап-меню 'Отзывы' не открылся (.tooltip-menu не найден)"
            )

    @allure.title("TC-0321s: Переход в Карты через попап 'Отзывы'. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Отзывы' → клик на 'Карты' в попапе.\n"
        "Критерий успеха: открылась страница Карты (URL содержит /home-pois)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0321_reviews_karty_popup_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Отзывы', дождаться попапа с пунктом 'Карты'"):
            side_menu.click_menu_item_reviews_narrow(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SUBMENU_ITEM_KARTY)

        with allure.step("Кликнуть на пункт 'Карты' в попапе"):
            side_menu.click_submenu_item_karty(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Карты (URL содержит /home-pois)"):
            side_menu.wait_url_contains(self.endpoints.HOME_POIS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.HOME_POIS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.HOME_POIS_ENDPOINT}"
            )

    @allure.title("TC-0322s: Переход на страницу Чаты. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Чаты'.\n"
        "Критерий успеха: открылась страница чатов (URL содержит /chats)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0322_chats_page_narrow_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Чаты'"):
            side_menu.click_menu_item_chats_narrow(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница чатов (URL содержит /chats)"):
            side_menu.wait_url_contains(self.endpoints.CHATS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.CHATS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.CHATS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0323s: Переход на страницу Товары. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Товары'.\n"
        "Критерий успеха: открылась страница Товары (URL содержит /products)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0323_products_page_narrow_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Товары'"):
            side_menu.click_menu_item_products_narrow(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Товары (URL содержит /products)"):
            side_menu.wait_url_contains(self.endpoints.PRODUCTS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PRODUCTS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.PRODUCTS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0324s: Переход на страницу Места. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Места'.\n"
        "Критерий успеха: открылась страница Места (URL содержит /pois)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0324_places_page_narrow_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Места'"):
            side_menu.click_menu_item_places_narrow(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Места (URL содержит /pois)"):
            side_menu.wait_url_contains(self.endpoints.POIS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.POIS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.POIS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0325s: Переход на страницу Клиенты. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Клиенты'.\n"
        "Критерий успеха: открылась страница Клиенты (URL содержит /clients)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0325_clients_page_narrow_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Клиенты'"):
            side_menu.click_menu_item_clients_narrow(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Клиенты (URL содержит /clients)"):
            side_menu.wait_url_contains(self.endpoints.CLIENTS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.CLIENTS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.CLIENTS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0326s: Раскрытие попап 'Аналитика' кликом. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Аналитика'.\n"
        "Критерий успеха: появился попап-меню с подпунктами Аналитики."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0326_analytics_popup_click_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Аналитика' в узком меню"):
            side_menu.click_menu_item_analytics_narrow(self.menu_locator)

        with allure.step("Проверить критерий: попап-меню Аналитики открылся (подпункт 'Отзывы' виден)"):
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_REVIEWS)
            self.assertion.assert_true(
                side_menu.is_narrow_popup_open(self.menu_locator),
                "Попап-меню Аналитики не открылся (.tooltip-menu не найден)"
            )

    @allure.title("TC-0327s: Раскрытие попап 'Аналитика' ховером. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: ховер на иконку 'Аналитика'.\n"
        "Критерий успеха: появился попап-меню с подпунктами Аналитики."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0327_analytics_popup_hover_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Ховер на иконку 'Аналитика' в узком меню"):
            side_menu.hover_menu_item_analytics_narrow(self.menu_locator)

        with allure.step("Проверить критерий: попап-меню Аналитики открылся (подпункт 'Отзывы' виден)"):
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_REVIEWS)
            self.assertion.assert_true(
                side_menu.is_narrow_popup_open(self.menu_locator),
                "Попап-меню Аналитики не открылся (.tooltip-menu не найден)"
            )

    @allure.title("TC-0328s: Переход на страницу Аналитика|Отзывы. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Аналитика', клик на подпункт 'Отзывы' в попапе.\n"
        "Критерий успеха: открылась страница Аналитика > Отзывы (URL содержит /review-analytics)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0328_analytics_reviews_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Аналитика', дождаться попапа"):
            side_menu.click_menu_item_analytics_narrow(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_REVIEWS)

        with allure.step("Кликнуть на подпункт 'Отзывы' в попапе"):
            side_menu.click_analytics_submenu_reviews(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Отзывы (URL содержит /review-analytics)"):
            side_menu.wait_url_contains(self.endpoints.REVIEW_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.REVIEW_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.REVIEW_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0329s: Переход на страницу Аналитика|Обработка. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Аналитика', клик на подпункт 'Обработка' в попапе.\n"
        "Критерий успеха: открылась страница Аналитика > Обработка (URL содержит /processing-analytics)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0329_analytics_processing_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Аналитика', дождаться попапа"):
            side_menu.click_menu_item_analytics_narrow(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_PROCESSING_NARROW)

        with allure.step("Кликнуть на подпункт 'Обработка' в попапе"):
            side_menu.click_on_elem(self.menu_locator.ANALYTICS_SUBMENU_PROCESSING_NARROW)

        with allure.step("Проверить критерий: открылась страница Аналитика > Обработка (URL содержит /processing-analytics)"):
            side_menu.wait_url_contains(self.endpoints.PROCESSING_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PROCESSING_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.PROCESSING_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0330s: Переход на страницу Аналитика|Инсайты. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Аналитика', клик на подпункт 'Инсайты' в попапе.\n"
        "Критерий успеха: открылась страница Аналитика > Инсайты (URL содержит /insights)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0330_analytics_insights_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Аналитика', дождаться попапа"):
            side_menu.click_menu_item_analytics_narrow(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_INSIGHTS)

        with allure.step("Кликнуть на подпункт 'Инсайты' в попапе"):
            side_menu.click_analytics_submenu_insights(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Инсайты (URL содержит /insights)"):
            side_menu.wait_url_contains(self.endpoints.INSIGHTS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.INSIGHTS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.INSIGHTS_ENDPOINT}"
            )

    @allure.title("TC-0331s: Переход на страницу Аналитика|Сравнение. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Аналитика', клик на подпункт 'Сравнение' в попапе.\n"
        "Критерий успеха: открылась страница Аналитика > Сравнение (URL содержит /comparison-analytics)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0331_analytics_comparison_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Аналитика', дождаться попапа"):
            side_menu.click_menu_item_analytics_narrow(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_COMPARISON)

        with allure.step("Кликнуть на подпункт 'Сравнение' в попапе"):
            side_menu.click_analytics_submenu_comparison(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Сравнение (URL содержит /comparison-analytics)"):
            side_menu.wait_url_contains(self.endpoints.COMPARISON_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.COMPARISON_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.COMPARISON_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0332s: Переход на страницу Настройки. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Настройки'.\n"
        "Критерий успеха: открылась страница Настройки (URL содержит /settings)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0332_settings_page_narrow_menu(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Настройки'"):
            side_menu.click_menu_item_settings_narrow(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Настройки (URL содержит /settings)"):
            side_menu.wait_url_contains(self.endpoints.SETTINGS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.SETTINGS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.SETTINGS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0333s: Раскрытие попап 'Нужна помощь?' кликом. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Нужна помощь?'.\n"
        "Критерий успеха: появилась кнопка 'Смотреть инструкции' в попапе."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0333_help_popup_click_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Нужна помощь?' в узком меню"):
            side_menu.click_help_menu(self.menu_locator)

        with allure.step("Проверить критерий: попап открылся — кнопка 'Смотреть инструкции' видима"):
            side_menu.wait_locator(self.menu_locator.HELP_INSTRUCTIONS_BTN)
            self.assertion.assert_true(
                side_menu.page.locator(self.menu_locator.HELP_INSTRUCTIONS_BTN).is_visible(),
                "Попап 'Нужна помощь?' не открылся (кнопка 'Смотреть инструкции' не найдена)"
            )

    @allure.title("TC-0334s: Раскрытие попап 'Нужна помощь?' ховером. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: ховер на иконку 'Нужна помощь?'.\n"
        "Критерий успеха: появилась кнопка 'Смотреть инструкции' в попапе."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0334_help_popup_hover_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Ховер на иконку 'Нужна помощь?' в узком меню"):
            side_menu.hover_help_menu(self.menu_locator)

        with allure.step("Проверить критерий: попап открылся — кнопка 'Смотреть инструкции' видима"):
            side_menu.wait_locator(self.menu_locator.HELP_INSTRUCTIONS_BTN)
            self.assertion.assert_true(
                side_menu.page.locator(self.menu_locator.HELP_INSTRUCTIONS_BTN).is_visible(),
                "Попап 'Нужна помощь?' не открылся (кнопка 'Смотреть инструкции' не найдена)"
            )

    @allure.title("TC-0335s: Раскрытие попап 'Профиль' кликом. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на блок профиля.\n"
        "Критерий успеха: появилась кнопка 'Мой профиль' в попапе."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0335_profile_popup_click_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на блок профиля в узком меню"):
            side_menu.click_profile_menu(self.menu_locator)

        with allure.step("Проверить критерий: попап открылся — кнопка 'Мой профиль' видима"):
            side_menu.wait_locator(self.menu_locator.PROFILE_MY_PROFILE_BTN)
            self.assertion.assert_true(
                side_menu.page.locator(self.menu_locator.PROFILE_MY_PROFILE_BTN).is_visible(),
                "Попап профиля не открылся (кнопка 'Мой профиль' не найдена)"
            )

    @allure.title("TC-0336s: Раскрытие попап 'Профиль' ховером. Узкое меню")
    @allure.description(
        "Пририквизиты: субадмин авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: ховер на блок профиля.\n"
        "Критерий успеха: появилась кнопка 'Мой профиль' в попапе."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0336_profile_popup_hover_narrow(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)
        side_menu = SideMenuPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(self.client_locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Ховер на блок профиля в узком меню"):
            side_menu.hover_profile_menu(self.menu_locator)

        with allure.step("Проверить критерий: попап открылся — кнопка 'Мой профиль' видима"):
            side_menu.wait_locator(self.menu_locator.PROFILE_MY_PROFILE_BTN)
            self.assertion.assert_true(
                side_menu.page.locator(self.menu_locator.PROFILE_MY_PROFILE_BTN).is_visible(),
                "Попап профиля не открылся (кнопка 'Мой профиль' не найдена)"
            )


@allure.feature("side_menu")
@allure.story("TS-03 Боковое меню")
class TestTS03SideMenuManager:
    data = UserData()
    endpoints = Endpoints()
    client_locator = ClientFilterLocators()
    menu_locator = SideMenuLocators()
    assertion = Assertions()

    @allure.title("TC-0302m: Раскрытие подменю Отзывы. Широкое меню")
    @allure.description(
        "Доступно для клиентов с маркетплейсами и картами.\n"
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент', "
        "боковое меню открыто (sidebar with-sidebar).\n"
        "Критерий успеха: подменю 'Отзывы' стало активным."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0302_submenu_reviews_wide_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Раскрыть пункт меню 'Отзывы' (item__link-text)"):
            side_menu.click_menu_item_reviews(self.menu_locator)

        with allure.step("Проверить, что подменю 'Отзывы' стало активным"):
            self.assertion.assert_true(
                side_menu.is_submenu_active(self.menu_locator),
                "Подменю 'Отзывы' не стало активным (router-link-active router-link-exact-active item__link-text)"
            )

    @allure.title("TC-0303m: Переход в отзывы Карт. Широкое меню")
    @allure.description(
        "Доступно для клиентов с маркетплейсами и картами.\n"
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент', "
        "боковое меню открыто (sidebar with-sidebar), "
        "пункт меню 'Отзывы' (item__link-text) открыт.\n"
        "Критерий успеха: aria-current='page' с текстом 'Карты'."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0303_reviews_karty_wide_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Открыть пункт меню 'Отзывы' (item__link-text)"):
            side_menu.click_menu_item_reviews(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SUBMENU_ACTIVE)

        with allure.step("Выбрать пункт подменю 'Карты' (item__link-text)"):
            side_menu.setup_skeleton_observer(self.menu_locator)
            side_menu.click_submenu_item_karty(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Карты (URL содержит /home-pois)"):
            side_menu.wait_url_contains(self.endpoints.HOME_POIS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.HOME_POIS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.HOME_POIS_ENDPOINT}"
            )

    @allure.title("TC-0304m: Переход на страницу Чаты. Широкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Чаты'.\n"
        "Критерий успеха: открытие страницы чатов (URL содержит /chats)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0304_chats_page_wide_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)

        with allure.step("Кликнуть на пункт меню 'Чаты'"):
            side_menu.click_menu_item_chats(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница чатов (URL содержит /chats)"):
            side_menu.wait_url_contains(self.endpoints.CHATS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.CHATS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.CHATS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0305m: Переход на страницу Товары. Широкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Товары'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Товары' (class=header__title)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0305_products_page_wide_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Товары'"):
            side_menu.click_menu_item_products(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Товары (URL содержит /products)"):
            side_menu.wait_url_contains(self.endpoints.PRODUCTS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PRODUCTS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.PRODUCTS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0306m: Переход на страницу Места. Широкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Места'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Места' (class=header__title)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0306_places_page_wide_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Места'"):
            side_menu.click_menu_item_places(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Места (URL содержит /pois)"):
            side_menu.wait_url_contains(self.endpoints.POIS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.POIS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.POIS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0308m: Раскрытие подменю Аналитика. Широкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика'.\n"
        "Критерий успеха: наличие подпункта 'Отзывы' (class=item__link-text is-inactive)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0308_analytics_submenu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Аналитика'"):
            side_menu.click_menu_item_analytics(self.menu_locator)

        with allure.step("Проверить критерий: появился подпункт 'Отзывы' в подменю Аналитика"):
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_REVIEWS)
            self.assertion.assert_true(
                side_menu.is_analytics_submenu_open(self.menu_locator),
                "Подменю Аналитика не раскрылось (подпункт 'Отзывы' с классом is-inactive не найден)"
            )

    @allure.title("TC-0309m: Переход на страницу Аналитика|Отзывы. Широкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Отзывы'.\n"
        "Критерий успеха: открыта страница Аналитика > Отзывы (analytics-section__header с текстом 'Отзывы')."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0309_analytics_reviews(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_REVIEWS)

        with allure.step("Кликнуть на подпункт подменю 'Отзывы'"):
            side_menu.click_analytics_submenu_reviews(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Отзывы (URL содержит /review-analytics)"):
            side_menu.wait_url_contains(self.endpoints.REVIEW_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.REVIEW_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.REVIEW_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0310m: Переход на страницу Аналитика|Обработка. Широкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Обработка'.\n"
        "Критерий успеха: открыта страница Аналитика > Обработка (analytics-section__header с текстом 'Обработка')."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0310_analytics_processing(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_PROCESSING)

        with allure.step("Кликнуть на подпункт подменю 'Обработка'"):
            side_menu.click_analytics_submenu_processing(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Обработка (URL содержит /processing-analytics)"):
            side_menu.wait_url_contains(self.endpoints.PROCESSING_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PROCESSING_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.PROCESSING_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0311m: Переход на страницу Аналитика|Инсайты. Широкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Инсайты'.\n"
        "Критерий успеха: открыта страница Аналитика > Инсайты (analytics-section__header с текстом 'Инсайты')."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0311_analytics_insights(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_INSIGHTS)

        with allure.step("Кликнуть на подпункт подменю 'Инсайты'"):
            side_menu.click_analytics_submenu_insights(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Инсайты (URL содержит /insights)"):
            side_menu.wait_url_contains(self.endpoints.INSIGHTS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.INSIGHTS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.INSIGHTS_ENDPOINT}"
            )

    @allure.title("TC-0312m: Переход на страницу Аналитика|Сравнение. Широкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Аналитика', клик на подпункт 'Сравнение'.\n"
        "Критерий успеха: открыта страница Аналитика > Сравнение (analytics-section__header с текстом 'Сравнение')."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0312_analytics_comparison(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Аналитика' для раскрытия подменю"):
            side_menu.click_menu_item_analytics(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_COMPARISON)

        with allure.step("Кликнуть на подпункт подменю 'Сравнение'"):
            side_menu.click_analytics_submenu_comparison(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Сравнение (URL содержит /comparison-analytics)"):
            side_menu.wait_url_contains(self.endpoints.COMPARISON_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.COMPARISON_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.COMPARISON_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0313m: Переход на страницу Настройки. Широкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: клик на пункт меню 'Настройки'.\n"
        "Критерий успеха: открытие страницы с заголовком 'Настройки' (class=header__title)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0313_settings_page_wide_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Кликнуть на пункт меню 'Настройки'"):
            side_menu.click_menu_item_settings(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Настройки (URL содержит /settings)"):
            side_menu.wait_url_contains(self.endpoints.SETTINGS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.SETTINGS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.SETTINGS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0314m: Переход в инструкции через ховер-меню 'Нужна помощь?'")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: ховер на 'Нужна помощь?' → клик 'Смотреть инструкции'.\n"
        "Критерий успеха: открылась новая вкладка с URL https://spix.ru/instructions/."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0314_instructions_hover_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Ховер на элемент 'Нужна помощь?' в сайдбаре"):
            side_menu.hover_help_menu(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.HELP_INSTRUCTIONS_BTN)

        with allure.step("Кликнуть 'Смотреть инструкции' и проверить новую вкладку"):
            new_tab_url = side_menu.wait_for_new_tab_and_get_url(self.menu_locator)
            self.assertion.assert_url(new_tab_url, self.endpoints.INSTRUCTIONS_URL)

    @allure.title("TC-0315m: Переход в техподдержку через ховер-меню 'Нужна помощь?'")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: ховер на 'Нужна помощь?' → клик 'Написать в поддержку'.\n"
        "Критерий успеха: переход на страницу /support."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0315_support_hover_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Ховер на элемент 'Нужна помощь?' в сайдбаре"):
            side_menu.hover_help_menu(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.HELP_SUPPORT_BTN)

        with allure.step("Кликнуть 'Написать в поддержку' и проверить URL"):
            side_menu.click_support(self.menu_locator)
            side_menu.wait_url(f"**{self.endpoints.SUPPORT_PAGE_ENDPOINT}")
            self.assertion.assert_true(
                self.endpoints.SUPPORT_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.SUPPORT_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0316m: Переход в профиль через ховер-меню профиля")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: ховер на профиль → клик 'Мой профиль'.\n"
        "Критерий успеха: переход на страницу /profile."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0316_profile_hover_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Ховер на блок профиля в футере сайдбара"):
            side_menu.hover_profile_menu(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.PROFILE_MY_PROFILE_BTN)

        with allure.step("Кликнуть 'Мой профиль' и проверить URL"):
            side_menu.click_my_profile(self.menu_locator)
            side_menu.wait_url_contains(self.endpoints.PROFILE_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PROFILE_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.PROFILE_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0337m: Переход на страницу Компания через ховер-меню профиля")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте.\n"
        "Действие: ховер на профиль → клик 'Компания'.\n"
        "Критерий успеха: переход на страницу /settings-company/settings."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0337_company_hover_menu(self, manager_page, manager_user_setup):
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)

        with allure.step("Ховер на блок профиля в футере сайдбара"):
            side_menu.hover_profile_menu(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.PROFILE_COMPANY_BTN)

        with allure.step("Кликнуть 'Компания' и проверить URL"):
            side_menu.click_company(self.menu_locator)
            side_menu.wait_url_contains(self.endpoints.SETTINGS_COMPANY_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.SETTINGS_COMPANY_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.SETTINGS_COMPANY_ENDPOINT}"
            )

    @allure.title("TC-0338m: Переход на страницу История обработки через ховер-меню профиля")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте.\n"
        "Действие: ховер на профиль → клик 'История обработки'.\n"
        "Критерий успеха: переход на страницу /statistic/month."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0338_history_hover_menu(self, manager_page, manager_user_setup):
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)

        with allure.step("Ховер на блок профиля в футере сайдбара"):
            side_menu.hover_profile_menu(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.PROFILE_HISTORY_BTN)

        with allure.step("Кликнуть 'История обработки' и проверить URL"):
            side_menu.click_history(self.menu_locator)
            side_menu.wait_url_contains(self.endpoints.STATISTIC_MONTH_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.STATISTIC_MONTH_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.STATISTIC_MONTH_ENDPOINT}"
            )

    @allure.title("TC-0317m: Выход из ЛК через ховер-меню профиля")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "в селекте header-client-filter__clients выбран клиент 'Лайковый клиент'.\n"
        "Действие: ховер на профиль → клик 'Выход' → подтверждение 'Да'.\n"
        "Критерий успеха: редирект на страницу авторизации /signin/."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0317_logout_hover_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)


        with allure.step("Ховер на блок профиля в футере сайдбара"):
            side_menu.hover_profile_menu(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.PROFILE_LOGOUT_BTN)

        with allure.step("Кликнуть 'Выход' в ховер-меню"):
            side_menu.click_logout(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.LOGOUT_CONFIRM_YES_BTN)

        with allure.step("Подтвердить выход — кликнуть 'Да' и проверить редирект на /signin/"):
            side_menu.click_confirm_logout(self.menu_locator)
            side_menu.wait_url_contains(self.endpoints.AUTHORIZATION_USER_ENDPOINT.rstrip('/'))
            self.assertion.assert_true(
                self.endpoints.AUTHORIZATION_USER_ENDPOINT.rstrip('/') in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.AUTHORIZATION_USER_ENDPOINT}"
            )


@allure.feature("side_menu")
@allure.story("TS-03 Боковое меню")
class TestTS03SideMenuNarrowManager:
    data = UserData()
    endpoints = Endpoints()
    client_locator = ClientFilterLocators()
    menu_locator = SideMenuLocators()
    assertion = Assertions()

    @allure.title("TC-0318m: Сворачивание бокового меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню широкое.\n"
        "Действие: клик на burger для сворачивания меню.\n"
        "Критерий успеха: боковое меню стало узким (.sidebar-wrapper.small)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0318_collapse_sidebar(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Раскрыть боковое меню, если оно узкое"):
            side_menu.expand_sidebar(self.menu_locator)

        with allure.step("Кликнуть burger для сворачивания бокового меню"):
            side_menu.click_on_elem(self.menu_locator.SIDEBAR_BURGER)

        with allure.step("Проверить критерий: боковое меню стало узким (.sidebar-wrapper.small)"):
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)
            self.assertion.assert_true(
                side_menu.is_sidebar_collapsed(self.menu_locator),
                "Боковое меню не свернулось (.sidebar-wrapper.small не найден)"
            )

    @allure.title("TC-0319m: Раскрытие попап 'Отзывы' кликом. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Отзывы'.\n"
        "Критерий успеха: появился попап-меню (.tooltip-menu)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0319_reviews_popup_click_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Отзывы' в узком меню"):
            side_menu.click_menu_item_reviews_narrow(self.menu_locator)

        with allure.step("Проверить критерий: попап-меню 'Отзывы' открылся (.tooltip-menu)"):
            side_menu.wait_locator(self.menu_locator.NARROW_POPUP)
            self.assertion.assert_true(
                side_menu.is_narrow_popup_open(self.menu_locator),
                "Попап-меню 'Отзывы' не открылся (.tooltip-menu не найден)"
            )

    @allure.title("TC-0320m: Раскрытие попап 'Отзывы' ховером. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: ховер на иконку 'Отзывы'.\n"
        "Критерий успеха: появился попап-меню (.tooltip-menu)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0320_reviews_popup_hover_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Ховер на иконку 'Отзывы' в узком меню"):
            side_menu.hover_menu_item_reviews_narrow(self.menu_locator)

        with allure.step("Проверить критерий: попап-меню 'Отзывы' открылся (.tooltip-menu)"):
            side_menu.wait_locator(self.menu_locator.NARROW_POPUP)
            self.assertion.assert_true(
                side_menu.is_narrow_popup_open(self.menu_locator),
                "Попап-меню 'Отзывы' не открылся (.tooltip-menu не найден)"
            )

    @allure.title("TC-0321m: Переход в Карты через попап 'Отзывы'. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Отзывы' → клик на 'Карты' в попапе.\n"
        "Критерий успеха: открылась страница Карты (URL содержит /home-pois)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0321_reviews_karty_popup_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Отзывы', дождаться попапа с пунктом 'Карты'"):
            side_menu.click_menu_item_reviews_narrow(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SUBMENU_ITEM_KARTY)

        with allure.step("Кликнуть на пункт 'Карты' в попапе"):
            side_menu.click_submenu_item_karty(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Карты (URL содержит /home-pois)"):
            side_menu.wait_url_contains(self.endpoints.HOME_POIS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.HOME_POIS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.HOME_POIS_ENDPOINT}"
            )

    @allure.title("TC-0322m: Переход на страницу Чаты. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Чаты'.\n"
        "Критерий успеха: открылась страница чатов (URL содержит /chats)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0322_chats_page_narrow_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()

        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Чаты'"):
            side_menu.click_menu_item_chats_narrow(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница чатов (URL содержит /chats)"):
            side_menu.wait_url_contains(self.endpoints.CHATS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.CHATS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.CHATS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0323m: Переход на страницу Товары. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Товары'.\n"
        "Критерий успеха: открылась страница Товары (URL содержит /products)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0323_products_page_narrow_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Товары'"):
            side_menu.click_menu_item_products_narrow(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Товары (URL содержит /products)"):
            side_menu.wait_url_contains(self.endpoints.PRODUCTS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PRODUCTS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.PRODUCTS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0324m: Переход на страницу Места. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Места'.\n"
        "Критерий успеха: открылась страница Места (URL содержит /pois)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0324_places_page_narrow_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Места'"):
            side_menu.click_menu_item_places_narrow(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Места (URL содержит /pois)"):
            side_menu.wait_url_contains(self.endpoints.POIS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.POIS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.POIS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0326m: Раскрытие попап 'Аналитика' кликом. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Аналитика'.\n"
        "Критерий успеха: появился попап-меню с подпунктами Аналитики."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0326_analytics_popup_click_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Аналитика' в узком меню"):
            side_menu.click_menu_item_analytics_narrow(self.menu_locator)

        with allure.step("Проверить критерий: попап-меню Аналитики открылся (подпункт 'Отзывы' виден)"):
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_REVIEWS)
            self.assertion.assert_true(
                side_menu.is_narrow_popup_open(self.menu_locator),
                "Попап-меню Аналитики не открылся (.tooltip-menu не найден)"
            )

    @allure.title("TC-0327m: Раскрытие попап 'Аналитика' ховером. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: ховер на иконку 'Аналитика'.\n"
        "Критерий успеха: появился попап-меню с подпунктами Аналитики."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0327_analytics_popup_hover_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Ховер на иконку 'Аналитика' в узком меню"):
            side_menu.hover_menu_item_analytics_narrow(self.menu_locator)

        with allure.step("Проверить критерий: попап-меню Аналитики открылся (подпункт 'Отзывы' виден)"):
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_REVIEWS)
            self.assertion.assert_true(
                side_menu.is_narrow_popup_open(self.menu_locator),
                "Попап-меню Аналитики не открылся (.tooltip-menu не найден)"
            )

    @allure.title("TC-0328m: Переход на страницу Аналитика|Отзывы. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Аналитика', клик на подпункт 'Отзывы' в попапе.\n"
        "Критерий успеха: открылась страница Аналитика > Отзывы (URL содержит /review-analytics)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0328_analytics_reviews_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Аналитика', дождаться попапа"):
            side_menu.click_menu_item_analytics_narrow(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_REVIEWS)

        with allure.step("Кликнуть на подпункт 'Отзывы' в попапе"):
            side_menu.click_analytics_submenu_reviews(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Отзывы (URL содержит /review-analytics)"):
            side_menu.wait_url_contains(self.endpoints.REVIEW_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.REVIEW_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.REVIEW_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0329m: Переход на страницу Аналитика|Обработка. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Аналитика', клик на подпункт 'Обработка' в попапе.\n"
        "Критерий успеха: открылась страница Аналитика > Обработка (URL содержит /processing-analytics)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0329_analytics_processing_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Аналитика', дождаться попапа"):
            side_menu.click_menu_item_analytics_narrow(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_PROCESSING)

        with allure.step("Кликнуть на подпункт 'Обработка' в попапе"):
            side_menu.click_analytics_submenu_processing(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Обработка (URL содержит /processing-analytics)"):
            side_menu.wait_url_contains(self.endpoints.PROCESSING_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PROCESSING_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.PROCESSING_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0330m: Переход на страницу Аналитика|Инсайты. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Аналитика', клик на подпункт 'Инсайты' в попапе.\n"
        "Критерий успеха: открылась страница Аналитика > Инсайты (URL содержит /insights)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0330_analytics_insights_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Аналитика', дождаться попапа"):
            side_menu.click_menu_item_analytics_narrow(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_INSIGHTS)

        with allure.step("Кликнуть на подпункт 'Инсайты' в попапе"):
            side_menu.click_analytics_submenu_insights(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Инсайты (URL содержит /insights)"):
            side_menu.wait_url_contains(self.endpoints.INSIGHTS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.INSIGHTS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.INSIGHTS_ENDPOINT}"
            )

    @allure.title("TC-0331m: Переход на страницу Аналитика|Сравнение. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Аналитика', клик на подпункт 'Сравнение' в попапе.\n"
        "Критерий успеха: открылась страница Аналитика > Сравнение (URL содержит /comparison-analytics)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0331_analytics_comparison_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Аналитика', дождаться попапа"):
            side_menu.click_menu_item_analytics_narrow(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.ANALYTICS_SUBMENU_COMPARISON)

        with allure.step("Кликнуть на подпункт 'Сравнение' в попапе"):
            side_menu.click_analytics_submenu_comparison(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Аналитика > Сравнение (URL содержит /comparison-analytics)"):
            side_menu.wait_url_contains(self.endpoints.COMPARISON_ANALYTICS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.COMPARISON_ANALYTICS_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.COMPARISON_ANALYTICS_ENDPOINT}"
            )

    @allure.title("TC-0332m: Переход на страницу Настройки. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Настройки'.\n"
        "Критерий успеха: открылась страница Настройки (URL содержит /settings)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0332_settings_page_narrow_menu(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Настройки'"):
            side_menu.click_menu_item_settings_narrow(self.menu_locator)

        with allure.step("Проверить критерий: открылась страница Настройки (URL содержит /settings)"):
            side_menu.wait_url_contains(self.endpoints.SETTINGS_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.SETTINGS_PAGE_ENDPOINT in side_menu.get_current_url(),
                f"URL не содержит {self.endpoints.SETTINGS_PAGE_ENDPOINT}"
            )

    @allure.title("TC-0333m: Раскрытие попап 'Нужна помощь?' кликом. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на иконку 'Нужна помощь?'.\n"
        "Критерий успеха: появилась кнопка 'Смотреть инструкции' в попапе."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0333_help_popup_click_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на иконку 'Нужна помощь?' в узком меню"):
            side_menu.click_help_menu(self.menu_locator)

        with allure.step("Проверить критерий: попап открылся — кнопка 'Смотреть инструкции' видима"):
            side_menu.wait_locator(self.menu_locator.HELP_INSTRUCTIONS_BTN)
            self.assertion.assert_true(
                side_menu.page.locator(self.menu_locator.HELP_INSTRUCTIONS_BTN).is_visible(),
                "Попап 'Нужна помощь?' не открылся (кнопка 'Смотреть инструкции' не найдена)"
            )

    @allure.title("TC-0334m: Раскрытие попап 'Нужна помощь?' ховером. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: ховер на иконку 'Нужна помощь?'.\n"
        "Критерий успеха: появилась кнопка 'Смотреть инструкции' в попапе."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0334_help_popup_hover_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Ховер на иконку 'Нужна помощь?' в узком меню"):
            side_menu.hover_help_menu(self.menu_locator)

        with allure.step("Проверить критерий: попап открылся — кнопка 'Смотреть инструкции' видима"):
            side_menu.wait_locator(self.menu_locator.HELP_INSTRUCTIONS_BTN)
            self.assertion.assert_true(
                side_menu.page.locator(self.menu_locator.HELP_INSTRUCTIONS_BTN).is_visible(),
                "Попап 'Нужна помощь?' не открылся (кнопка 'Смотреть инструкции' не найдена)"
            )

    @allure.title("TC-0335m: Раскрытие попап 'Профиль' кликом. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: клик на блок профиля.\n"
        "Критерий успеха: появилась кнопка 'Мой профиль' в попапе."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0335_profile_popup_click_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Кликнуть на блок профиля в узком меню"):
            side_menu.click_profile_menu(self.menu_locator)

        with allure.step("Проверить критерий: попап открылся — кнопка 'Мой профиль' видима"):
            side_menu.wait_locator(self.menu_locator.PROFILE_MY_PROFILE_BTN)
            self.assertion.assert_true(
                side_menu.page.locator(self.menu_locator.PROFILE_MY_PROFILE_BTN).is_visible(),
                "Попап профиля не открылся (кнопка 'Мой профиль' не найдена)"
            )

    @allure.title("TC-0336m: Раскрытие попап 'Профиль' ховером. Узкое меню")
    @allure.description(
        "Пририквизиты: менеджер авторизован на сайте, "
        "выбран клиент 'Лайковый клиент', боковое меню узкое.\n"
        "Действие: ховер на блок профиля.\n"
        "Критерий успеха: появилась кнопка 'Мой профиль' в попапе."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0336_profile_popup_hover_narrow(self, manager_page, manager_user_setup):
        client_nm = manager_user_setup["client_nm"]
        reviews_page = ReviewsPage(manager_page)
        side_menu = SideMenuPage(manager_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()


        with allure.step("Свернуть боковое меню до узкого"):
            side_menu.collapse_sidebar(self.menu_locator)
            side_menu.wait_locator(self.menu_locator.SIDEBAR_COLLAPSED)

        with allure.step("Ховер на блок профиля в узком меню"):
            side_menu.hover_profile_menu(self.menu_locator)

        with allure.step("Проверить критерий: попап открылся — кнопка 'Мой профиль' видима"):
            side_menu.wait_locator(self.menu_locator.PROFILE_MY_PROFILE_BTN)
            self.assertion.assert_true(
                side_menu.page.locator(self.menu_locator.PROFILE_MY_PROFILE_BTN).is_visible(),
                "Попап профиля не открылся (кнопка 'Мой профиль' не найдена)"
            )


@allure.feature("side_menu")
@allure.story("TS-03 Хедер меню оператора")
class TestTS03HeaderMenuOperator:
    data = UserData()
    endpoints = Endpoints()
    op_locator = OperatorLocators()
    assertion = Assertions()


    @allure.title("TC-03001o: Переход в Отзывы карт через dropdown источника в шапке")
    @allure.description(
        "Пририквизиты: оператор авторизован, клиент с источниками Маркетплейсы и Карты.\n"
        "Действие: кликнуть 'Маркетплейсы' → выбрать 'Карты'.\n"
        "Критерий: URL содержит /home-pois."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_03001_reviews_karty_header_source(self, operator_page, operator_user_setup):
        op = OperatorPage(operator_page)

        with allure.step("Открыть страницу отзывов"):
            op.open()

        with allure.step("Кликнуть на кнопку источника 'Маркетплейсы' в шапке"):
            op.click_source_btn(self.op_locator)
            op.wait_locator(self.op_locator.SOURCE_OPTION_KARTY)

        with allure.step("Кликнуть на 'Карты' в dropdown и проверить URL"):
            op.click_karty_option(self.op_locator)
            op.wait_url_contains(self.endpoints.HOME_POIS_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.HOME_POIS_ENDPOINT in op.get_current_url(),
                f"URL не содержит {self.endpoints.HOME_POIS_ENDPOINT}"
            )

    @allure.title("TC-03003o: Переход в Мой профиль через меню профиля в шапке")
    @allure.description(
        "Пририквизиты: оператор авторизован на сайте.\n"
        "Действие: открыть страницу Отзывов, ховер на иконку профиля → клик 'Мой профиль'.\n"
        "Критерий успеха: URL содержит /profile."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_03003_my_profile_header_menu(self, operator_page, operator_user_setup):
        op = OperatorPage(operator_page)

        with allure.step("Открыть страницу отзывов"):
            op.open()

        with allure.step("Ховер и клик на иконку профиля в шапке"):
            op.hover_profile_menu(self.op_locator)
            op.click_profile_menu(self.op_locator)
            op.wait_locator(self.op_locator.PROFILE_MY_PROFILE_BTN)

        with allure.step("Кликнуть 'Мой профиль' и проверить URL"):
            op.click_my_profile(self.op_locator)
            op.wait_url_contains(self.endpoints.PROFILE_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.PROFILE_PAGE_ENDPOINT in op.get_current_url(),
                f"URL не содержит {self.endpoints.PROFILE_PAGE_ENDPOINT}"
            )

    @allure.title("TC-03004o: Переход на страницу инструкций через меню профиля в шапке")
    @allure.description(
        "Пририквизиты: оператор авторизован на сайте.\n"
        "Действие: открыть страницу Отзывов, ховер на иконку профиля → клик 'Смотреть инструкции'.\n"
        "Критерий успеха: открылась новая вкладка с URL https://spix.ru/instructions/."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_03004_instructions_header_menu(self, operator_page, operator_user_setup):
        op = OperatorPage(operator_page)

        with allure.step("Открыть страницу отзывов"):
            op.open()

        with allure.step("Ховер и клик на иконку профиля в шапке"):
            op.hover_profile_menu(self.op_locator)
            op.click_profile_menu(self.op_locator)
            op.wait_locator(self.op_locator.PROFILE_INSTRUCTIONS_BTN)

        with allure.step("Кликнуть 'Смотреть инструкции' и проверить новую вкладку"):
            new_tab_url = op.wait_for_new_tab_and_get_url(self.op_locator)
            self.assertion.assert_url(new_tab_url, self.endpoints.INSTRUCTIONS_URL)

    @allure.title("TC-03005o: Переход в поддержку через меню профиля в шапке")
    @allure.description(
        "Пририквизиты: оператор авторизован на сайте.\n"
        "Действие: открыть страницу Отзывов, ховер на иконку профиля → клик 'Написать в поддержку'.\n"
        "Критерий успеха: URL содержит /support."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_03005_support_header_menu(self, operator_page, operator_user_setup):
        op = OperatorPage(operator_page)

        with allure.step("Открыть страницу отзывов"):
            op.open()

        with allure.step("Ховер и клик на иконку профиля в шапке"):
            op.hover_profile_menu(self.op_locator)
            op.click_profile_menu(self.op_locator)
            op.wait_locator(self.op_locator.PROFILE_SUPPORT_BTN)

        with allure.step("Кликнуть 'Написать в поддержку' и проверить URL"):
            op.click_support(self.op_locator)
            op.wait_url_contains(self.endpoints.SUPPORT_PAGE_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.SUPPORT_PAGE_ENDPOINT in op.get_current_url(),
                f"URL не содержит {self.endpoints.SUPPORT_PAGE_ENDPOINT}"
            )

    @allure.title("TC-03006o: Переход в историю обработки через меню профиля в шапке")
    @allure.description(
        "Пририквизиты: оператор авторизован на сайте.\n"
        "Действие: открыть страницу Отзывов, ховер на иконку профиля → клик 'История обработки'.\n"
        "Критерий успеха: URL содержит /statistic (для fresh-пользователя может быть /statistic "
        "без /month, т.к. Vue-роутер редиректит при отсутствии истории)."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_03006_history_header_menu(self, operator_page, operator_user_setup):
        op = OperatorPage(operator_page)

        with allure.step("Открыть страницу отзывов"):
            op.open()

        with allure.step("Ховер и клик на иконку профиля в шапке"):
            op.hover_profile_menu(self.op_locator)
            op.click_profile_menu(self.op_locator)
            op.wait_locator(self.op_locator.PROFILE_HISTORY_BTN)

        with allure.step("Кликнуть 'История обработки' и проверить URL"):
            op.click_history(self.op_locator)
            op.wait_url_contains(self.endpoints.STATISTIC_ENDPOINT)
            self.assertion.assert_true(
                self.endpoints.STATISTIC_ENDPOINT in op.get_current_url(),
                f"URL не содержит {self.endpoints.STATISTIC_ENDPOINT}"
            )

    @allure.title("TC-03007o: Выход из ЛК через меню профиля в шапке")
    @allure.description(
        "Пририквизиты: оператор авторизован на сайте.\n"
        "Действие: открыть страницу Отзывов, ховер на иконку профиля → 'Выход' → подтверждение 'Да'.\n"
        "Критерий успеха: редирект на страницу авторизации /signin/."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_03007_logout_header_menu(self, operator_page, operator_user_setup):
        op = OperatorPage(operator_page)

        with allure.step("Открыть страницу отзывов"):
            op.open()

        with allure.step("Ховер и клик на иконку профиля в шапке"):
            op.hover_profile_menu(self.op_locator)
            op.click_profile_menu(self.op_locator)
            op.wait_locator(self.op_locator.PROFILE_LOGOUT_BTN)

        with allure.step("Кликнуть 'Выход' в меню профиля"):
            op.click_logout(self.op_locator)
            op.wait_locator(self.op_locator.LOGOUT_CONFIRM_YES_BTN)

        with allure.step("Подтвердить выход — кликнуть 'Да' и проверить редирект на /signin/"):
            op.click_confirm_logout(self.op_locator)
            op.wait_url_contains(self.endpoints.AUTHORIZATION_USER_ENDPOINT.rstrip('/'))
            self.assertion.assert_true(
                self.endpoints.AUTHORIZATION_USER_ENDPOINT.rstrip('/') in op.get_current_url(),
                f"URL не содержит {self.endpoints.AUTHORIZATION_USER_ENDPOINT}"
            )
