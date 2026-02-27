import pytest
from playwright.sync_api import Playwright, ViewportSize
from locators.authorization_locators import UserAuthorization
from locators.clients_page_locators import ClientsPageLocators
from locators.user_management_locators import UserManagementLocators
from data.dataclasses.user_dataclass import UserData
from data.dataclasses.manager_auth_dataclass import ManagerAuthData
from pages.authorization_page import UserAuthorizationPage
from pages.clients_page import ClientsPage
from pages.user_management_page import UserManagementPage
from data.endpoints import Endpoints

data = UserData()
user_authorization = UserAuthorization()
clients_locator = ClientsPageLocators()
endpoint = Endpoints()

@pytest.fixture()
def page(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(
        viewport=ViewportSize(width=1440, height=980),
        base_url="https://go.dev.spix.ru/"
    )
    page = context.new_page()
    yield page
    page.wait_for_timeout(3000)
    page.close()
    context.close()
    browser.close()

@pytest.fixture(scope="session")
def get_cookies(playwright: Playwright):
    phone_number = data.PHONE_NUMBER
    password = data.PASSWORD
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        base_url='https://go.dev.spix.ru/'
    )
    page = context.new_page()
    page.goto('/')
    page.locator(user_authorization.PHONE_FIELD_LOC).fill(phone_number)
    page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(password)
    page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
    page.wait_for_timeout(2000)
    cookies = context.cookies()
    page.close()
    context.close()
    browser.close()
    return cookies


@pytest.fixture()
def authorized_user(playwright: Playwright, get_cookies):
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(
        viewport=ViewportSize(width=1440, height=980),
        base_url="https://go.dev.spix.ru/"
    )
    context.add_cookies(get_cookies)
    page = context.new_page()
    yield page
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope="session")
def subadmin_context(playwright: Playwright):
    """Авторизует субадмина один раз и хранит контекст на всю сессию"""
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(
        viewport=ViewportSize(width=1440, height=980),
        base_url="https://go.dev.spix.ru/"
    )
    page = context.new_page()
    page.goto("/")
    page.locator(user_authorization.PHONE_FIELD_LOC).fill(data.SUBADMIN_PHONE_NUMBER)
    page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(data.SUBADMIN_PASSWORD)
    page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
    page.locator(user_authorization.CODE_FIRST_DIGIT_LOC).wait_for(state="visible")
    page.locator(user_authorization.CODE_FIRST_DIGIT_LOC).click()
    page.locator(user_authorization.CODE_FIRST_DIGIT_LOC).fill(data.SMS_CODE[0])
    for i in range(5):
        page.locator(user_authorization.CODE_5DIGITS_LOC).nth(i).fill(data.SMS_CODE[i + 1])
    page.locator(user_authorization.ENTER_BUTTON_LOC).click()
    page.wait_for_url("**/1?**")
    page.close()
    yield context
    context.close()
    browser.close()


@pytest.fixture()
def subadmin_page(subadmin_context):
    """Создаёт новую страницу в уже авторизованном контексте"""
    page = subadmin_context.new_page()
    yield page
    page.close()


@pytest.fixture()
def client_page(playwright: Playwright):
    """Авторизуется под субадмином, создаёт клиента, переходит к форме добавления пользователя"""
    manager_data = ManagerAuthData()
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(
        viewport=ViewportSize(width=1440, height=980),
        base_url="https://go.dev.spix.ru/"
    )
    page = context.new_page()

    full_url = data.BASE_URL + endpoint.AUTHORIZATION_USER_ENDPOINT
    auth_page = UserAuthorizationPage(page, full_url)
    auth_page.open()
    auth_page.authorization_user_wildcard(
        user_authorization,
        data.SUBADMIN_PHONE_NUMBER,
        data.SUBADMIN_PASSWORD
    )

    clients_url = data.BASE_URL + endpoint.CLIENTS_ENDPOINT
    clients_page = ClientsPage(page, clients_url)
    clients_page.open()
    clients_page.wait_locator(clients_locator.ADD_CLIENT_BTN)

    clients_page.create_client(
        clients_locator,
        manager_data.CLIENT_NAME,
        manager_data.CLIENT_EMAIL
    )

    clients_page.click_first_client(manager_data.CLIENT_NAME)
    clients_page.navigate_to_add_user(clients_locator)

    yield page

    page.wait_for_timeout(3000)
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope="class")
def managers_by_language(playwright: Playwright):
    """Создаёт клиента с 3 менеджерами (по одному на каждый язык), возвращает dict {язык: (phone, password)}"""
    user_mgmt_locator = UserManagementLocators()
    languages = ["Русский", "English", "Indonesia"]
    managers = {}

    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(
        viewport=ViewportSize(width=1440, height=980),
        base_url="https://go.dev.spix.ru/"
    )
    page = context.new_page()

    full_url = data.BASE_URL + endpoint.AUTHORIZATION_USER_ENDPOINT
    auth_page = UserAuthorizationPage(page, full_url)
    auth_page.open()
    auth_page.authorization_user_wildcard(
        user_authorization,
        data.SUBADMIN_PHONE_NUMBER,
        data.SUBADMIN_PASSWORD
    )

    clients_url = data.BASE_URL + endpoint.CLIENTS_ENDPOINT
    clients_page = ClientsPage(page, clients_url)
    clients_page.open()
    clients_page.wait_locator(clients_locator.ADD_CLIENT_BTN)

    client_data = ManagerAuthData()
    clients_page.create_client(
        clients_locator,
        client_data.CLIENT_NAME,
        client_data.CLIENT_EMAIL
    )
    clients_page.click_first_client(client_data.CLIENT_NAME)
    clients_page.navigate_to_add_user(clients_locator)

    for lang in languages:
        mgr = ManagerAuthData()
        user_mgmt_page = UserManagementPage(page)
        user_mgmt_page.create_user(
            user_mgmt_locator,
            mgr.MANAGER_NAME,
            mgr.MANAGER_EMAIL,
            mgr.MANAGER_PHONE,
            mgr.MANAGER_PASSWORD,
            "Менеджер"
        )

        user_mgmt_page.click_user_by_name(mgr.MANAGER_NAME)
        user_mgmt_page.change_language(user_mgmt_locator, lang)
        user_mgmt_page.click_save_edit()

        managers[lang] = (mgr.MANAGER_PHONE, mgr.MANAGER_PASSWORD)

        clients_page.navigate_to_add_user(clients_locator)

    yield page, managers

    page.wait_for_timeout(3000)
    page.close()
    context.close()
    browser.close()
