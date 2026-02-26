import allure
import pytest
from locators.authorization_locators import UserAuthorization
from locators.clients_page_locators import ClientsPageLocators
from locators.user_management_locators import UserManagementLocators
from pages.authorization_page import UserAuthorizationPage
from pages.clients_page import ClientsPage
from pages.user_management_page import UserManagementPage
from data.endpoints import Endpoints
from data.dataclasses.user_dataclass import UserData
from data.dataclasses.manager_auth_dataclass import ManagerAuthData
from utils.assertions.assertions import Assertions

@allure.feature('User Authorization')
@allure.story('Login')
class TestUserAuthorization:
    locator = UserAuthorization()
    clients_locator = ClientsPageLocators()
    user_mgmt_locator = UserManagementLocators()
    endpoint = Endpoints()
    assertions = Assertions()
    data = UserData()
    manager_data = ManagerAuthData()

    @allure.title("TC-0101s: Successful subadmin authorization")
    @allure.description("Verify that subadmin can successfully log in with valid credentials and redirect to feedback page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0101s_successful_authorization(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Perform subadmin authorization"):
            auth_page.authorization_user(self.locator, self.data.SUBADMIN_PHONE_NUMBER, self.data.SUBADMIN_PASSWORD)
        with allure.step("Verify redirect to feedback page"):
            expected_url = self.data.BASE_URL + self.endpoint.FEEDBACK_PAGE_ENDPOINT
            self.assertions.assert_url(page.url, expected_url)

    @allure.title("TC-0102: No redirect after authorization with wrong password")
    @allure.description("Verify that user stays on signin page after entering wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0102_no_redirect_with_wrong_password(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Enter valid phone and wrong password, click submit"):
            auth_page.authorization_with_wrong_password(
                self.locator, self.data.SUBADMIN_PHONE_NUMBER, self.data.WRONG_PASSWORD
            )
        with allure.step("Verify URL remains on signin page"):
            expected_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            self.assertions.assert_url(
                page.url.rstrip('/'), expected_url.rstrip('/')
            )

    @allure.title("TC-0103: Error toast on authorization with wrong password")
    @allure.description("Verify that error toast is displayed after entering wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0103_error_toast_with_wrong_password(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Enter valid phone and wrong password, click submit"):
            auth_page.authorization_with_wrong_password(
                self.locator, self.data.SUBADMIN_PHONE_NUMBER, self.data.WRONG_PASSWORD
            )
        with allure.step("Verify error toast message is displayed"):
            error_text = auth_page.get_error_toast_text(self.locator)
            self.assertions.assert_text(error_text, self.data.ERROR_MESSAGE_PASSWORD)

    @allure.title("TC-0104: No redirect after authorization with wrong phone number")
    @allure.description("Verify that user stays on signin page after entering wrong phone number")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0104_no_redirect_with_wrong_phone(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Enter wrong phone and valid password, click submit"):
            auth_page.authorization_with_wrong_password(
                self.locator, self.data.WRONG_PHONE_NUMBER, self.data.SUBADMIN_PASSWORD
            )
        with allure.step("Verify URL remains on signin page"):
            expected_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            self.assertions.assert_url(
                page.url.rstrip('/'), expected_url.rstrip('/')
            )

    @allure.title("TC-0105: Error toast on authorization with wrong phone number")
    @allure.description("Verify that error toast is displayed after entering wrong phone number")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0105_error_toast_with_wrong_phone(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Enter wrong phone and valid password, click submit"):
            auth_page.authorization_with_wrong_password(
                self.locator, self.data.WRONG_PHONE_NUMBER, self.data.SUBADMIN_PASSWORD
            )
        with allure.step("Verify error toast message is displayed"):
            error_text = auth_page.get_error_toast_text(self.locator)
            self.assertions.assert_text(error_text, self.data.ERROR_MESSAGE_PASSWORD)

    @allure.title("TC-0106: Phone placeholder changes after selecting Kazakhstan")
    @allure.description("Verify that phone placeholder updates to Kazakhstan format after country switch")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0106_phone_placeholder_changes_to_kazakhstan(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Select Kazakhstan from country dropdown"):
            auth_page.select_country(self.locator, self.locator.COUNTRY_NAME_KAZAKHSTAN)
        with allure.step("Verify phone placeholder changed to Kazakhstan format"):
            placeholder = auth_page.get_phone_placeholder(self.locator)
            self.assertions.assert_text(placeholder, self.data.KAZAKHSTAN_PHONE_PLACEHOLDER)

    @allure.title("TC-0107: Country flag changes after selecting Kazakhstan")
    @allure.description("Verify that country flag updates to Kazakhstan after country switch")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0107_country_flag_changes_to_kazakhstan(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Select Kazakhstan from country dropdown"):
            auth_page.select_country(self.locator, self.locator.COUNTRY_NAME_KAZAKHSTAN)
        with allure.step("Verify flag changed to Kazakhstan"):
            flag_class = auth_page.get_country_flag_class(self.locator)
            self.assertions.assert_text(flag_class, self.data.KAZAKHSTAN_FLAG_CLASS)

    @allure.title("TC-0108: Language switch changes page texts [{language}]")
    @allure.description("Verify that switching language updates all page texts to the selected language")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("language", ["English", "Indonesia", "Русский"],
                             ids=["english", "indonesia", "russian"])
    def test_tc_0108_language_switch(self, page, language):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step(f"Switch language to {language}"):
            auth_page.select_language(self.locator, language)
        with allure.step(f"Verify page texts match {language} translation"):
            expected = self.data.LANG_TRANSLATIONS[language]
            actual_texts = {
                "title": auth_page.get_signin_title(self.locator),
                "description": auth_page.get_signin_description(self.locator),
                "phone_label": auth_page.get_phone_label(self.locator),
                "password_label": auth_page.get_password_label(self.locator),
                "recover_pass": auth_page.get_recover_pass_text(self.locator),
            }
            self.assertions.assert_page_texts(actual_texts, expected)

    @allure.title("TC-0109: Return to authorization page from SMS code page")
    @allure.description("Verify that clicking return button on SMS page navigates back to authorization form")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0109_return_from_sms_page(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Submit valid credentials to reach SMS code page"):
            auth_page.submit_credentials(
                self.locator, self.data.SUBADMIN_PHONE_NUMBER, self.data.SUBADMIN_PASSWORD
            )
        with allure.step("Click return to authorization button"):
            auth_page.click_return_to_signin(self.locator)
        with allure.step("Verify authorization form is displayed"):
            phone_label = auth_page.get_phone_label(self.locator)
            self.assertions.assert_text(phone_label, "Телефон")

    @allure.title("TC-0110: Resend SMS code after timer expires")
    @allure.description("Verify that resending SMS code shows confirmation text and restarts the timer")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0110_resend_sms_code(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Submit valid credentials to reach SMS code page"):
            auth_page.submit_credentials(
                self.locator, self.data.SUBADMIN_PHONE_NUMBER, self.data.SUBADMIN_PASSWORD
            )
        with allure.step("Wait for resend timer to expire"):
            auth_page.wait_resend_code_available(self.locator)
        with allure.step("Click resend code button"):
            auth_page.click_resend_code(self.locator)
        with allure.step("Verify code sent confirmation and timer are displayed"):
            code_sent_text = auth_page.get_code_sent_text(self.locator)
            self.assertions.assert_text(code_sent_text, self.data.CODE_SENT_TEXT)

    @allure.title("TC-0111: Support button opens support page")
    @allure.description("Verify that clicking 'Нужна помощь?' button redirects to the support page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0111_support_button_opens_support_page(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Click 'Нужна помощь?' button"):
            auth_page.click_support_btn(self.locator)
        with allure.step("Verify redirect to support page"):
            expected_url = self.data.BASE_URL + self.endpoint.SUPPORT_SIGNIN_ENDPOINT
            self.assertions.assert_url(page.url, expected_url)

    @allure.title("TC-0112: Recover password link opens password recovery page")
    @allure.description("Verify that clicking 'Восстановить пароль' link redirects to the password recovery page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0112_recover_password_link(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Click 'Восстановить пароль' link"):
            auth_page.click_recover_pass(self.locator)
        with allure.step("Verify redirect to password recovery page"):
            expected_url = self.data.BASE_URL + self.endpoint.PASS_RECOVERY_ENDPOINT
            self.assertions.assert_url(page.url, expected_url)

    @allure.title("TC-0113: Password recovery sends confirmation email")
    @allure.description("Verify that submitting email on password recovery page shows confirmation text and displays the email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0113_password_recovery_confirmation(self, page):
        with allure.step("Open password recovery page"):
            full_url = self.data.BASE_URL + self.endpoint.PASS_RECOVERY_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Enter email and submit recovery form"):
            auth_page.submit_recovery_email(self.locator, self.data.RECOVERY_EMAIL)
        with allure.step("Verify confirmation text and email are displayed"):
            actual_texts = {
                "description": auth_page.get_recovery_description(self.locator),
                "email": auth_page.get_recovery_email(self.locator),
            }
            expected_texts = {
                "description": self.data.RECOVERY_CONFIRMATION_TEXT,
                "email": self.data.RECOVERY_EMAIL,
            }
            self.assertions.assert_page_texts(actual_texts, expected_texts)

    @allure.title("TC-0114: Return to authorization page from password recovery page")
    @allure.description("Verify that clicking 'Авторизация' link on password recovery page navigates back to signin")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0114_return_from_recovery_page(self, page):
        with allure.step("Open password recovery page"):
            full_url = self.data.BASE_URL + self.endpoint.PASS_RECOVERY_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Click 'Авторизация' link to return"):
            auth_page.click_recovery_return_to_signin(self.locator)
        with allure.step("Verify redirect to authorization page"):
            expected_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            self.assertions.assert_url(
                page.url.rstrip('/'), expected_url.rstrip('/')
            )

    @allure.title("TC-0115m: Успешная авторизация менеджера")
    @allure.description(
        "Авторизация под субадмином, создание клиента, "
        "создание менеджера для клиента, "
        "авторизация под созданным менеджером."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0115m_successful_manager_authorization(self, page):
        with allure.step("Открыть страницу авторизации и войти под субадмином"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
            auth_page.authorization_user_wildcard(
                self.locator,
                self.data.SUBADMIN_PHONE_NUMBER,
                self.data.SUBADMIN_PASSWORD
            )

        with allure.step("Перейти на страницу Клиенты"):
            clients_url = self.data.BASE_URL + self.endpoint.CLIENTS_ENDPOINT
            clients_page = ClientsPage(page, clients_url)
            clients_page.open()
            clients_page.wait_locator(self.clients_locator.ADD_CLIENT_BTN)

        with allure.step(f"Создать клиента '{self.manager_data.CLIENT_NAME}'"):
            clients_page.create_client(
                self.clients_locator,
                self.manager_data.CLIENT_NAME,
                self.manager_data.CLIENT_EMAIL
            )

        with allure.step("Открыть созданного клиента"):
            clients_page.click_first_client(self.manager_data.CLIENT_NAME)

        with allure.step("Перейти к форме добавления пользователя"):
            clients_page.navigate_to_add_user(self.clients_locator)

        with allure.step(f"Создать менеджера '{self.manager_data.MANAGER_NAME}'"):
            user_mgmt_page = UserManagementPage(page)
            user_mgmt_page.create_manager(
                self.user_mgmt_locator,
                self.manager_data.MANAGER_NAME,
                self.manager_data.MANAGER_EMAIL,
                self.manager_data.MANAGER_PHONE,
                self.manager_data.MANAGER_PASSWORD
            )

        with allure.step("Перейти на страницу авторизации"):
            page.context.clear_cookies()
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()

        with allure.step("Авторизоваться под созданным менеджером"):
            auth_page.authorization_user_wildcard(
                self.locator,
                self.manager_data.MANAGER_PHONE,
                self.manager_data.MANAGER_PASSWORD
            )

        with allure.step("Проверить успешную авторизацию менеджера"):
            self.assertions.assert_true(
                "feedbacks_tab=pending" in page.url,
                f"Менеджер не перенаправлен на страницу отзывов. Текущий URL: {page.url}"
            )
