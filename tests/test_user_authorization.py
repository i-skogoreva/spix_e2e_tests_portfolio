import allure
import pytest
from locators.authorization_locators import UserAuthorization
from pages.authorization_page import UserAuthorizationPage
from data.endpoints import Endpoints
from data.dataclasses.user_dataclass import UserData
from utils.assertions.assertions import Assertions

@allure.feature('User Authorization')
@allure.story('Login')
class TestUserAuthorization:
    locator = UserAuthorization()
    endpoint = Endpoints()
    assertions = Assertions()
    data = UserData()

    @allure.title("TC-0001: Successful user authorization [{role}]")
    @allure.description("Verify that user can successfully log in with valid credentials and redirect to feedback page")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("role, phone, password", [
        ("subadmin", UserData.SUBADMIN_PHONE_NUMBER, UserData.SUBADMIN_PASSWORD),
        ("manager", UserData.MANAGER_PHONE_NUMBER, UserData.MANAGER_PASSWORD),
        ("operator", UserData.OPERATOR_PHONE_NUMBER, UserData.OPERATOR_PASSWORD),
    ], ids=["subadmin", "manager", "operator"])
    def test_tc_0001_successful_authorization(self, page, role, phone, password):
        with allure.step(f"Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step(f"Perform {role} authorization"):
            auth_page.authorization_user(self.locator, phone, password)
        with allure.step("Verify redirect to feedback page"):
            expected_url = self.data.BASE_URL + self.endpoint.FEEDBACK_PAGE_ENDPOINT
            self.assertions.assert_url(page.url, expected_url)

    @allure.title("TC-0002: No redirect after authorization with wrong password")
    @allure.description("Verify that user stays on signin page after entering wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0002_no_redirect_with_wrong_password(self, page):
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

    @allure.title("TC-0003: Error toast on authorization with wrong password")
    @allure.description("Verify that error toast is displayed after entering wrong password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0003_error_toast_with_wrong_password(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Enter valid phone and wrong password, click submit"):
            auth_page.authorization_with_wrong_password(
                self.locator, self.data.SUBADMIN_PASSWORD, self.data.WRONG_PASSWORD
            )
        with allure.step("Verify error toast message is displayed"):
            error_text = auth_page.get_error_toast_text(self.locator)
            self.assertions.assert_text(error_text, self.data.ERROR_MESSAGE_PASSWORD)

    @allure.title("TC-0004: No redirect after authorization with wrong phone number")
    @allure.description("Verify that user stays on signin page after entering wrong phone number")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0004_no_redirect_with_wrong_phone(self, page):
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

    @allure.title("TC-0005: Error toast on authorization with wrong phone number")
    @allure.description("Verify that error toast is displayed after entering wrong phone number")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0005_error_toast_with_wrong_phone(self, page):
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

    @allure.title("TC-0006: Phone placeholder changes after selecting Kazakhstan")
    @allure.description("Verify that phone placeholder updates to Kazakhstan format after country switch")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0006_phone_placeholder_changes_to_kazakhstan(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Select Kazakhstan from country dropdown"):
            auth_page.select_country(self.locator, self.locator.COUNTRY_NAME_KAZAKHSTAN)
        with allure.step("Verify phone placeholder changed to Kazakhstan format"):
            placeholder = auth_page.get_phone_placeholder(self.locator)
            self.assertions.assert_text(placeholder, self.data.KAZAKHSTAN_PHONE_PLACEHOLDER)

    @allure.title("TC-0007: Country flag changes after selecting Kazakhstan")
    @allure.description("Verify that country flag updates to Kazakhstan after country switch")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0007_country_flag_changes_to_kazakhstan(self, page):
        with allure.step("Open authorization page"):
            full_url = self.data.BASE_URL + self.endpoint.AUTHORIZATION_USER_ENDPOINT
            auth_page = UserAuthorizationPage(page, full_url)
            auth_page.open()
        with allure.step("Select Kazakhstan from country dropdown"):
            auth_page.select_country(self.locator, self.locator.COUNTRY_NAME_KAZAKHSTAN)
        with allure.step("Verify flag changed to Kazakhstan"):
            flag_class = auth_page.get_country_flag_class(self.locator)
            self.assertions.assert_text(flag_class, self.data.KAZAKHSTAN_FLAG_CLASS)

    @allure.title("TC-0008: Language switch changes page texts [{language}]")
    @allure.description("Verify that switching language updates all page texts to the selected language")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("language", ["English", "Indonesia", "Русский"],
                             ids=["english", "indonesia", "russian"])
    def test_tc_0008_language_switch(self, page, language):
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
