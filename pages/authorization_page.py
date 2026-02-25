
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

    def select_language(self, locator, language_name):
         self.page.locator(locator.LANG_DROPDOWN_TOGGLE_LOC).dispatch_event("mousedown")
         self.page.locator(locator.LANG_OPTION_LOC, has_text=language_name).click()

    def get_signin_title(self, locator):
         return self.page.locator(locator.SIGNIN_TITLE_LOC).first.text_content()

    def get_signin_description(self, locator):
         return self.page.locator(locator.SIGNIN_DESCRIPTION_LOC).first.text_content()

    def get_phone_label(self, locator):
         return self.get_text(locator.PHONE_LABEL_LOC)

    def get_password_label(self, locator):
         return self.get_text(locator.PASSWORD_LABEL_LOC)

    def get_recover_pass_text(self, locator):
         return self.get_text(locator.RECOVER_PASS_LOC)

    def submit_credentials(self, locator, phone_number, password):
         self.fill_text(locator.PHONE_FIELD_LOC, phone_number)
         self.fill_text(locator.PASSWORD_FIELD_LOC, password)
         self.click_on_elem(locator.SUBMIT_BUTTON_LOC)
         self.wait_locator(locator.CODE_FIRST_DIGIT_LOC)

    def click_return_to_signin(self, locator):
         self.click_on_elem(locator.RETURN_TO_SIGNIN_LOC)
         self.wait_locator(locator.PHONE_LABEL_LOC)

    def wait_resend_code_available(self, locator):
         self.wait_locator(locator.RESEND_CODE_BTN_LOC, timeout=70000)

    def click_resend_code(self, locator):
         self.click_on_elem(locator.RESEND_CODE_BTN_LOC)
         self.wait_locator(locator.CODE_SENT_LOC)

    def get_code_sent_text(self, locator):
         return self.get_text(locator.CODE_SENT_LOC).strip()

    def is_resend_timer_visible(self, locator):
         return self.page.locator(locator.RESEND_TIMER_LOC).is_visible()

    def click_support_btn(self, locator):
         self.click_on_elem(locator.SUPPORT_BTN_LOC)

    def click_recover_pass(self, locator):
         self.click_on_elem(locator.RECOVER_PASS_LOC)

    def click_recovery_return_to_signin(self, locator):
         self.click_on_elem(locator.RETURN_TO_SIGNIN_LOC)

    def submit_recovery_email(self, locator, email):
         self.fill_text(locator.EMAIL_INPUT_LOC, email)
         self.click_on_elem(locator.PASS_RECOVERY_SUBMIT_LOC)
         self.wait_url(data.BASE_URL + endpoint.PASS_RECOVERY_SEND_ENDPOINT)

    def get_recovery_description(self, locator):
         return self.page.locator(locator.RECOVERY_DESCRIPTION_LOC).first.text_content()

    def get_recovery_email(self, locator):
         return self.get_text(locator.RECOVERY_EMAIL_LOC)