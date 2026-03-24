import allure
import pytest
from locators.authorization_locators import UserAuthorization
from locators.user_management_locators import UserManagementLocators
from pages.authorization_page import UserAuthorizationPage
from pages.user_management_page import UserManagementPage
from data.endpoints import Endpoints
from data.dataclasses.user_dataclass import UserData
from data.dataclasses.manager_auth_dataclass import ManagerAuthData
from data.dataclasses.operator_auth_dataclass import OperatorAuthData
from utils.assertions.assertions import Assertions

@allure.feature('Авторизация пользователя')
@allure.story('Вход в систему')
class TestUserAuthorization:
    locator = UserAuthorization()
    user_mgmt_locator = UserManagementLocators()
    endpoint = Endpoints()
    assertions = Assertions()
    data = UserData()
    manager_data = ManagerAuthData()
    operator_data = OperatorAuthData()

    @allure.title("TC-0101s: Успешная авторизация субадмина")
    @allure.description("Проверка успешного входа субадмина с валидными учётными данными и редирект на страницу отзывов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0101s_successful_authorization(self, page):
        with allure.step("Открыть страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Выполнить авторизацию субадмина"):
            auth_page.authorization_user(self.locator, self.data.SUBADMIN_PHONE_NUMBER, self.data.SUBADMIN_PASSWORD)
        with allure.step("Проверить редирект на страницу отзывов"):
            expected_url = self.data.BASE_URL + self.endpoint.FEEDBACK_PAGE_ENDPOINT
            self.assertions.assert_url(page.url, expected_url)

    @allure.title("TC-0102: Отсутствие редиректа при авторизации с неверным паролем")
    @allure.description("Проверка, что пользователь остаётся на странице авторизации после ввода неверного пароля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0102_no_redirect_with_wrong_password(self, page):
        with allure.step("Открыть страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Ввести валидный телефон и неверный пароль, нажать 'Войти'"):
            auth_page.authorization_with_wrong_password(
                self.locator, self.data.SUBADMIN_PHONE_NUMBER, self.data.WRONG_PASSWORD
            )
        with allure.step("Проверить, что URL остаётся на странице авторизации"):
            expected_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            self.assertions.assert_url(
                page.url.rstrip('/'), expected_url.rstrip('/')
            )

    @allure.title("TC-0103: Toast-ошибка при авторизации с неверным паролем")
    @allure.description("Проверка отображения toast-уведомления об ошибке после ввода неверного пароля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0103_error_toast_with_wrong_password(self, page):
        with allure.step("Открыть страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Ввести валидный телефон и неверный пароль, нажать 'Войти'"):
            auth_page.authorization_with_wrong_password(
                self.locator, self.data.SUBADMIN_PHONE_NUMBER, self.data.WRONG_PASSWORD
            )
        with allure.step("Проверить отображение toast-ошибки"):
            error_text = auth_page.get_error_toast_text(self.locator)
            self.assertions.assert_text(error_text, self.data.ERROR_MESSAGE_PASSWORD)

    @allure.title("TC-0104: Отсутствие редиректа при авторизации с неверным номером телефона")
    @allure.description("Проверка, что пользователь остаётся на странице авторизации после ввода неверного номера телефона")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0104_no_redirect_with_wrong_phone(self, page):
        with allure.step("Открыть страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Ввести неверный телефон и валидный пароль, нажать 'Войти'"):
            auth_page.authorization_with_wrong_password(
                self.locator, self.data.WRONG_PHONE_NUMBER, self.data.SUBADMIN_PASSWORD
            )
        with allure.step("Проверить, что URL остаётся на странице авторизации"):
            expected_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            self.assertions.assert_url(
                page.url.rstrip('/'), expected_url.rstrip('/')
            )

    @allure.title("TC-0105: Toast-ошибка при авторизации с неверным номером телефона")
    @allure.description("Проверка отображения toast-уведомления об ошибке после ввода неверного номера телефона")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0105_error_toast_with_wrong_phone(self, page):
        with allure.step("Открыть страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Ввести неверный телефон и валидный пароль, нажать 'Войти'"):
            auth_page.authorization_with_wrong_password(
                self.locator, self.data.WRONG_PHONE_NUMBER, self.data.SUBADMIN_PASSWORD
            )
        with allure.step("Проверить отображение toast-ошибки"):
            error_text = auth_page.get_error_toast_text(self.locator)
            self.assertions.assert_text(error_text, self.data.ERROR_MESSAGE_PASSWORD)

    @allure.title("TC-0106: Смена placeholder телефона при выборе Казахстана")
    @allure.description("Проверка, что placeholder поля телефона меняется на казахстанский формат после выбора страны")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0106_phone_placeholder_changes_to_kazakhstan(self, page):
        with allure.step("Открыть страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Выбрать Казахстан из выпадающего списка стран"):
            auth_page.select_country(self.locator, self.locator.COUNTRY_NAME_KAZAKHSTAN)
        with allure.step("Проверить, что placeholder изменился на казахстанский формат"):
            placeholder = auth_page.get_phone_placeholder(self.locator)
            self.assertions.assert_text(placeholder, self.data.KAZAKHSTAN_PHONE_PLACEHOLDER)

    @allure.title("TC-0107: Смена флага страны при выборе Казахстана")
    @allure.description("Проверка, что флаг страны меняется на казахстанский после выбора страны")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0107_country_flag_changes_to_kazakhstan(self, page):
        with allure.step("Открыть страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Выбрать Казахстан из выпадающего списка стран"):
            auth_page.select_country(self.locator, self.locator.COUNTRY_NAME_KAZAKHSTAN)
        with allure.step("Проверить, что флаг изменился на казахстанский"):
            flag_class = auth_page.get_country_flag_class(self.locator)
            self.assertions.assert_text(flag_class, self.data.KAZAKHSTAN_FLAG_CLASS)

    @allure.title("TC-0108: Смена языка меняет тексты страницы [{language}]")
    @allure.description("Проверка, что переключение языка обновляет все тексты страницы на выбранный язык")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("language", ["English", "Indonesia", "Русский"],
                             ids=["english", "indonesia", "russian"])
    def test_tc_0108_language_switch(self, page, language):
        with allure.step("Открыть страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step(f"Переключить язык на {language}"):
            auth_page.select_language(self.locator, language)
        with allure.step(f"Проверить, что тексты страницы соответствуют языку {language}"):
            expected = self.data.LANG_TRANSLATIONS[language]
            actual_texts = {
                "title": auth_page.get_signin_title(self.locator),
                "description": auth_page.get_signin_description(self.locator),
                "phone_label": auth_page.get_phone_label(self.locator),
                "password_label": auth_page.get_password_label(self.locator),
                "recover_pass": auth_page.get_recover_pass_text(self.locator),
            }
            self.assertions.assert_page_texts(actual_texts, expected)

    @allure.title("TC-0109: Кнопка 'Нужна помощь?' открывает страницу поддержки")
    @allure.description("Проверка, что нажатие кнопки 'Нужна помощь?' перенаправляет на страницу техподдержки")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0109_support_button_opens_support_page(self, page):
        with allure.step("Открыть страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Нажать кнопку 'Нужна помощь?'"):
            auth_page.click_support_btn(self.locator)
        with allure.step("Проверить редирект на страницу поддержки"):
            expected_url = self.data.BASE_URL + self.endpoint.SUPPORT_SIGNIN_ENDPOINT
            self.assertions.assert_url(page.url, expected_url)

    @allure.title("TC-0110: Ссылка 'Восстановить пароль' открывает страницу восстановления")
    @allure.description("Проверка, что нажатие ссылки 'Восстановить пароль' перенаправляет на страницу восстановления пароля")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0110_recover_password_link(self, page):
        with allure.step("Открыть страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Нажать ссылку 'Восстановить пароль'"):
            auth_page.click_recover_pass(self.locator)
        with allure.step("Проверить редирект на страницу восстановления пароля"):
            expected_url = self.data.BASE_URL + self.endpoint.PASS_RECOVERY_ENDPOINT
            self.assertions.assert_url(page.url, expected_url)

    @allure.title("TC-0111: Восстановление пароля отправляет подтверждение на email")
    @allure.description("Проверка, что после отправки email на странице восстановления пароля отображается подтверждение")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0111_password_recovery_confirmation(self, page):
        with allure.step("Открыть страницу восстановления пароля"):
            full_url = self.data.BASE_URL + self.endpoint.PASS_RECOVERY_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Ввести email и отправить форму восстановления"):
            auth_page.submit_recovery_email(self.locator, self.data.RECOVERY_EMAIL)
        with allure.step("Проверить отображение подтверждения и email"):
            actual_texts = {
                "description": auth_page.get_recovery_description(self.locator),
                "email": auth_page.get_recovery_email(self.locator),
            }
            expected_texts = {
                "description": self.data.RECOVERY_CONFIRMATION_TEXT,
                "email": self.data.RECOVERY_EMAIL,
            }
            self.assertions.assert_page_texts(actual_texts, expected_texts)

    @allure.title("TC-0112: Возврат на страницу авторизации со страницы восстановления пароля")
    @allure.description("Проверка, что нажатие ссылки '← Авторизация' на странице восстановления пароля возвращает на страницу входа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0112_return_from_recovery_page(self, page):
        with allure.step("Открыть страницу восстановления пароля"):
            full_url = self.data.BASE_URL + self.endpoint.PASS_RECOVERY_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Нажать ссылку '← Авторизация'"):
            auth_page.click_recovery_return_to_signin(self.locator)
        with allure.step("Проверить редирект на страницу авторизации"):
            expected_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            self.assertions.assert_url(
                page.url.rstrip('/'), expected_url.rstrip('/')
            )

    @allure.title("TC-0113m: Успешная авторизация менеджера")
    @allure.description(
        "Авторизация под субадмином, создание клиента (фикстура), "
        "создание менеджера для клиента, "
        "авторизация под созданным менеджером."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0113m_successful_manager_authorization(self, client_page):
        with allure.step(f"Создать менеджера '{self.manager_data.MANAGER_NAME}'"):
            user_mgmt_page = UserManagementPage(client_page)
            user_mgmt_page.create_user(
                self.user_mgmt_locator,
                self.manager_data.MANAGER_NAME,
                self.manager_data.MANAGER_EMAIL,
                self.manager_data.MANAGER_PHONE,
                self.manager_data.MANAGER_PASSWORD,
                "Менеджер"
            )

        with allure.step("Перейти на страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            client_page.context.clear_cookies()
            auth_page = UserAuthorizationPage(client_page, full_url)
            auth_page.open()

        with allure.step("Авторизоваться под созданным менеджером"):
            auth_page.authorization_user_wildcard(
                self.locator,
                self.manager_data.MANAGER_PHONE,
                self.manager_data.MANAGER_PASSWORD
            )

        with allure.step("Проверить успешную авторизацию менеджера"):
            self.assertions.assert_true(
                "feedbacks_tab=pending" in client_page.url,
                f"Менеджер не перенаправлен на страницу отзывов. Текущий URL: {client_page.url}"
            )

    @allure.title("TC-0114o: Успешная авторизация оператора")
    @allure.description(
        "Авторизация под субадмином, создание клиента (фикстура), "
        "создание оператора для клиента, "
        "авторизация под созданным оператором."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0114o_successful_operator_authorization(self, client_page):
        with allure.step(f"Создать оператора '{self.operator_data.OPERATOR_NAME}'"):
            user_mgmt_page = UserManagementPage(client_page)
            user_mgmt_page.create_user(
                self.user_mgmt_locator,
                self.operator_data.OPERATOR_NAME,
                self.operator_data.OPERATOR_EMAIL,
                self.operator_data.OPERATOR_PHONE,
                self.operator_data.OPERATOR_PASSWORD,
                "Оператор"
            )

        with allure.step("Перейти на страницу авторизации"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            client_page.context.clear_cookies()
            auth_page = UserAuthorizationPage(client_page, full_url)
            auth_page.open()

        with allure.step("Авторизоваться под созданным оператором"):
            auth_page.authorization_user_wildcard(
                self.locator,
                self.operator_data.OPERATOR_PHONE,
                self.operator_data.OPERATOR_PASSWORD
            )

        with allure.step("Проверить успешную авторизацию оператора"):
            self.assertions.assert_true(
                "feedbacks_tab=pending" in client_page.url,
                f"Оператор не перенаправлен на страницу отзывов. Текущий URL: {client_page.url}"
            )
