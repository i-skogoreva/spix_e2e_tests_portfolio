class BasePage:

    def __init__(self, page, url):
        self.page = page
        self.url = url

    def open(self):
        self.page.goto(self.url)

    def fill_text(self, loc, text_data):
        self.page.locator(loc).fill(text_data)

    def click_on_elem(self, loc):
        self.page.locator(loc).click()

    def get_text(self,loc):
        text = self.page.locator(loc).text_content()
        return text

    def get_all_text(self, loc):
        text = self.page.locator(loc).all_text_contents()
        return text

    def wait_url(self, url):
        self.page.wait_for_url(url)

    def get_attribute(self, loc, attribute):
        return self.page.locator(loc).get_attribute(attribute)

    def wait_locator(self, locator, timeout=15000):
        self.page.locator(locator).wait_for(
        state="visible",
        timeout=timeout
        )