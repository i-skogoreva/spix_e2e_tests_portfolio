import allure

from locators.client_filter_locators import ClientFilterLocators
from pages.reviews_page import ReviewsPage
from data.dataclasses.user_dataclass import UserData
from utils.assertions.assertions import Assertions

data = UserData()
locator = ClientFilterLocators()
assertion = Assertions()


@allure.suite("TS-03 Смена клиента")
class TestTS03ClientManagement:

    @allure.title("TC-0301s: Смена клиента")
    @allure.description(
        "Пререквизит: субадмин авторизован на сайте.\n"
        "Переход в клиента с именем 'Лайковый клиент'.\n"
        "Критерий: перезагрузка страницы и отображение клиента в селекте."
    )
    def test_TC0301_change_client(self, subadmin_page):
        reviews_page = ReviewsPage(subadmin_page)

        with allure.step("Открыть страницу отзывов"):
            reviews_page.open()
            reviews_page.wait_locator(locator.CLIENT_DROPDOWN_TOGGLE)

        with allure.step(f"Найти header-client-filter__clients и выбрать клиента '{data.CLIENT_LAYKOVY}'"):
            reviews_page.select_client(locator, data.CLIENT_LAYKOVY)

        with allure.step("Проверить появление лоадера при смене клиента"):
            reviews_page.wait_loader_visible(locator)

        with allure.step("Дождаться исчезновения лоадера (страница отзывов перезагружена)"):
            reviews_page.wait_loader_hidden(locator)

        with allure.step(f"Проверить, что клиент '{data.CLIENT_LAYKOVY}' отображается в селекте"):
            selected_client = reviews_page.get_selected_client(locator)
            assertion.assert_text(selected_client, data.CLIENT_LAYKOVY)
