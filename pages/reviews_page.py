from pages.base_page import BasePage
from data.endpoints import Endpoints

endpoints = Endpoints()


class ReviewsPage(BasePage):

    def __init__(self, page):
        super().__init__(page, endpoints.FEEDBACK_PAGE_ENDPOINT)

    def select_client(self, loc, client_name: str):
        """Открывает дропдаун, ищет клиента по имени и выбирает его"""
        self.click_on_elem(loc.CLIENT_DROPDOWN_TOGGLE)
        self.fill_text(loc.CLIENT_SEARCH_INPUT, client_name)
        option_loc = loc.CLIENT_OPTION_TEMPLATE.format(client_name=client_name)
        self.wait_locator(option_loc)
        self.click_on_elem(option_loc)

    def wait_loader_visible(self, loc, timeout: int = 5000):
        """Ожидает появления лоадера после смены клиента"""
        self.page.locator(loc.PAGE_LOADER).wait_for(state="visible", timeout=timeout)

    def wait_loader_hidden(self, loc, timeout: int = 15000):
        """Ожидает исчезновения лоадера (страница загружена)"""
        self.page.locator(loc.PAGE_LOADER).wait_for(state="hidden", timeout=timeout)

    def get_selected_client(self, loc) -> str:
        """Возвращает имя текущего выбранного клиента из селекта"""
        return self.get_text(loc.CLIENT_SELECTED)
