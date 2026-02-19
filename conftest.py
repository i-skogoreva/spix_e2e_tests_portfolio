import pytest
from playwright.sync_api import Playwright, ViewportSize
from locators.authorization_locators import UserAuthorization
from data.dataclasses.user_dataclass import UserData

data = UserData()
user_authorization = UserAuthorization()

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
