from pages.base_page import BasePage


class ClientsPage(BasePage):

    def __init__(self, page, url=""):
        super().__init__(page, url)

    def click_add_client(self, locator):
        self.page.wait_for_load_state("networkidle")
        self.page.locator(locator.ADD_CLIENT_BTN).scroll_into_view_if_needed()
        self.page.locator(locator.ADD_CLIENT_BTN).click(force=True)

    def fill_client_name(self, locator, name):
        self.wait_locator(locator.CLIENT_NAME_INPUT, timeout=30000)
        self.fill_text(locator.CLIENT_NAME_INPUT, name)

    def fill_client_email(self, locator, email):
        self.fill_text(locator.CLIENT_EMAIL_INPUT, email)

    def click_add_btn(self):
        self.page.locator(".popup button.button-main", has_text="Добавить").click()

    def create_client(self, locator, name, email):
        self.click_add_client(locator)
        self.fill_client_name(locator, name)
        self.fill_client_email(locator, email)
        self.click_add_btn()
        self.page.locator(".popup").wait_for(state="hidden", timeout=10000)

    def click_first_client(self, name):
        self.page.locator(".item-cell", has_text=name).first.click()
        self.page.wait_for_url("**/settings-company/**")

    def _click_client_action_btn(self, locator, client_name: str, btn_selector: str):
        """Находит строку клиента по имени и кликает кнопку внутри неё."""
        row = self.page.locator(".table-row").filter(
            has=self.page.locator(".item-cell", has_text=client_name)
        ).first
        row.locator(btn_selector).click()

    def click_client_reviews(self, locator, client_name: str):
        self._click_client_action_btn(locator, client_name, locator.BTN_CLIENT_REVIEWS)

    def click_client_products(self, locator, client_name: str):
        self._click_client_action_btn(locator, client_name, locator.BTN_CLIENT_PRODUCTS)

    def click_client_maps(self, locator, client_name: str):
        self._click_client_action_btn(locator, client_name, locator.BTN_CLIENT_MAPS)

    def click_client_brands(self, locator, client_name: str):
        self._click_client_action_btn(locator, client_name, locator.BTN_CLIENT_BRANDS)

    def click_client_templates(self, locator, client_name: str):
        self._click_client_action_btn(locator, client_name, locator.BTN_CLIENT_TEMPLATES)

    def click_client_users(self, locator, client_name: str):
        self._click_client_action_btn(locator, client_name, locator.BTN_CLIENT_USERS)

    def click_client_settings(self, locator, client_name: str):
        self._click_client_action_btn(locator, client_name, locator.BTN_CLIENT_SETTINGS)

    def click_client_billing(self, locator, client_name: str):
        self._click_client_action_btn(locator, client_name, locator.BTN_CLIENT_BILLING)

    def navigate_to_add_user(self, locator):
        if "/users" not in self.page.url:
            self.click_on_elem(locator.USERS_TAB)
            self.page.wait_for_timeout(2000)
        if "/add-user" not in self.page.url:
            current_url = self.page.url
            add_user_url = current_url.replace("/users?", "/users/add-user?")
            self.page.goto(add_user_url, wait_until="domcontentloaded")
            self.page.wait_for_load_state("domcontentloaded")