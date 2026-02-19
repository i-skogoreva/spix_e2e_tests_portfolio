
from locators.authorization_locators import UserAuthorization
from pages.base_page import BasePage
from data.dataclasses.user_dataclass import UserData
from data.endpoints import Endpoints

endpoint = Endpoints()
data = UserData()
locator = UserAuthorization()

class UserAuthorizationPage(BasePage):

    def authorization_user(self, locator, phone_number, password):
         self.fill_text(locator.PHONE_FIELD_LOC, phone_number)
         self.fill_text(locator.PASSWORD_FIELD_LOC, password)
         self.click_on_elem(locator.SUBMIT_BUTTON_LOC)
         self.wait_locator(locator.CODE_FIRST_DIGIT_LOC)
         self.click_on_elem(locator.CODE_FIRST_DIGIT_LOC)
         self.fill_text(locator.CODE_FIRST_DIGIT_LOC, data.SMS_CODE[0])
         for i in range(5):
             self.page.locator(locator.CODE_5DIGITS_LOC).nth(i).fill(data.SMS_CODE[i + 1])
         self.click_on_elem(locator.ENTER_BUTTON_LOC)
         self.wait_url(data.BASE_URL + endpoint.FEEDBACK_PAGE_ENDPOINT)

    def authorization_with_wrong_password(self, locator, phone, wrong_password):
         self.fill_text(locator.PHONE_FIELD_LOC, phone)
         self.fill_text(locator.PASSWORD_FIELD_LOC, wrong_password)
         self.click_on_elem(locator.SUBMIT_BUTTON_LOC)
         self.wait_locator(locator.ERROR_TOAST_LOC)

    def get_error_toast_text(self, locator):
         return self.get_text(locator.ERROR_TOAST_LOC)

    def select_country(self, locator, country_name):
         self.click_on_elem(locator.COUNTRY_DROPDOWN_LOC)
         self.page.locator(f".vti__dropdown-item:has(strong:text('{country_name}'))").first.click()

    def get_phone_placeholder(self, locator):
         return self.get_attribute(locator.PHONE_INPUT_LOC, "placeholder")

    def get_country_flag_class(self, locator):
         return self.get_attribute(locator.COUNTRY_FLAG_LOC, "class")