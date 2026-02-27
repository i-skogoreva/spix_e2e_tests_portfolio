import re

from pages.base_page import BasePage


class UserManagementPage(BasePage):

    def __init__(self, page, url=""):
        super().__init__(page, url)

    def fill_name(self, locator, name):
        self.wait_locator(locator.NAME_INPUT)
        self.fill_text(locator.NAME_INPUT, name)

    def fill_email(self, locator, email):
        self.fill_text(locator.EMAIL_INPUT, email)

    def fill_phone(self, locator, phone):
        self.fill_text(locator.PHONE_INPUT, phone)

    def fill_password(self, locator, password):
        self.page.locator(locator.PASSWORD_INPUT).nth(0).fill(password)
        self.page.locator(locator.PASSWORD_INPUT).nth(1).fill(password)

    def select_role(self, locator, role_name):
        self.click_on_elem(locator.ROLE_DROPDOWN_TOGGLE)
        self.page.locator(locator.ROLE_OPTION, has_text=role_name).click()

    def click_save(self):
        self.page.locator("button.button-main", has_text="Сохранить").click()

    def create_user(self, locator, name, email, phone, password, role):
        self.fill_name(locator, name)
        self.fill_email(locator, email)
        self.fill_phone(locator, phone)
        self.fill_password(locator, password)
        self.select_role(locator, role)
        self.click_save()
        self.page.wait_for_url("**/settings-company/users**", wait_until="networkidle", timeout=15000)

    def click_user_by_name(self, name):
        self.page.locator(".item-cell", has_text=name).first.click()
        self.page.wait_for_url("**/edit-user**")
        self.page.wait_for_load_state("networkidle")

    def change_language(self, locator, language_name):
        lang_toggle = self.page.locator(locator.LANGUAGE_DROPDOWN_TOGGLE)
        lang_toggle.scroll_into_view_if_needed()
        lang_toggle.click()
        self.page.wait_for_timeout(500)
        self.page.locator(".vs__dropdown-option", has_text=language_name).first.click()
        self.page.wait_for_timeout(500)
        selected = self.page.locator(".users-grid__language .vs__selected").text_content()
        assert selected.strip() == language_name, (
            f"Язык не изменён: ожидали '{language_name}', выбран '{selected.strip()}'"
        )

    def click_save_edit(self):
        self.page.locator("button.button-main", has_text="Сохранить").click()
        self.page.wait_for_url(
            re.compile(r".*/settings-company/users\?"),
            wait_until="networkidle",
            timeout=15000
        )
