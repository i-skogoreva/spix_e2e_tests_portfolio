from pages.base_page import BasePage


class FinanceManagementPage(BasePage):

    def __init__(self, page, url=""):
        super().__init__(page, url)

    def open_billing_for_client(self, base_url, client_id, upgrade_locator=None):
        """Открывает страницу биллинга для конкретного клиента по URL.

        Для свежего клиента биллинг может быть недоступен сразу —
        повторяет загрузку до 8 раз, пока кнопка 'Улучшить' не станет видимой.
        """
        billing_url = f"{base_url}/settings-company/billing?client_id={client_id}"
        for _ in range(8):
            self.page.goto(billing_url, timeout=30000)
            try:
                self.page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            if upgrade_locator:
                try:
                    self.page.locator(upgrade_locator).wait_for(
                        state="visible", timeout=5000
                    )
                    return
                except Exception:
                    self.page.wait_for_timeout(5000)
            else:
                return

    def click_upgrade(self, locator):
        """Нажимает кнопку 'Улучшить' и ждёт переход на страницу выбора тарифа."""
        self.page.locator(locator.UPGRADE_BTN).wait_for(
            state="visible", timeout=10000
        )
        self.page.locator(locator.UPGRADE_BTN).click()
        self.page.wait_for_url("**/billing-plan**", timeout=15000)
        try:
            self.page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass

    def select_free_plan(self, locator, plan_btn_locator):
        """Выбирает бесплатный пробный тариф: скролл к секции, клик, подтверждение.

        Args:
            locator: объект с общими локаторами (FREE_PLANS_SECTION, CONFIRM_BTN, SUCCESS_BTN)
            plan_btn_locator: CSS-селектор кнопки 'Подключить' конкретного тарифа
        """
        self.page.locator(locator.FREE_PLANS_SECTION).scroll_into_view_if_needed()
        # nth(1) — вторая кнопка 'Подключить' (первая в платном разделе)
        self.page.locator(plan_btn_locator).nth(1).click()
        self.page.locator(locator.CONFIRM_BTN).wait_for(
            state="visible", timeout=10000
        )
        self.page.locator(locator.CONFIRM_BTN).click()
        self.page.locator(locator.SUCCESS_BTN).wait_for(
            state="visible", timeout=10000
        )
        self.page.locator(locator.SUCCESS_BTN).click()
        self.page.wait_for_url("**/settings-company/billing**", timeout=15000)
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass

    def get_package_balance(self, locator):
        """Возвращает текущий остаток токенов (первое число из '100 из 100')."""
        import re
        self.page.locator(locator.PACKAGE_BALANCE).wait_for(
            state="visible", timeout=10000
        )
        text = self.page.locator(locator.PACKAGE_BALANCE).inner_text()
        # Текст вида "100  из  100" — берём первое число
        numbers = re.findall(r"\d+", text.replace("\xa0", "").replace(" ", ""))
        return int(numbers[0]) if numbers else 0

    def add_tokens(self, locator, amount, comment, base_url=None, client_id=None,
                   balance_before=None):
        """Открывает модалку добавления токенов, заполняет и подтверждает.

        После сохранения бэкенд обрабатывает токены асинхронно —
        метод повторяет навигацию на биллинг до 5 раз, ожидая изменения баланса.
        """
        self.page.locator(locator.ADD_TOKENS_BTN).click()
        self.page.locator(locator.TOKEN_AMOUNT_INPUT).wait_for(
            state="visible", timeout=10000
        )
        # Заполняем количество токенов
        amount_el = self.page.locator(locator.TOKEN_AMOUNT_INPUT)
        amount_el.click()
        amount_el.fill(amount)
        amount_el.evaluate("""el => {
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }""")
        # Заполняем комментарий
        comment_el = self.page.locator(locator.TOKEN_COMMENT_INPUT)
        comment_el.click()
        comment_el.fill(comment)
        comment_el.evaluate("""el => {
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }""")
        self.page.wait_for_timeout(500)
        self.page.locator(locator.TOKEN_SAVE_BTN).click()
        # Ждём закрытия модалки
        self.page.locator(locator.TOKEN_AMOUNT_INPUT).wait_for(
            state="hidden", timeout=10000
        )
        # Бэкенд обрабатывает токены асинхронно — повторяем навигацию
        if base_url and client_id and balance_before is not None:
            billing_url = f"{base_url}/settings-company/billing?client_id={client_id}"
            for _ in range(5):
                self.page.wait_for_timeout(5000)
                self.page.goto(billing_url, timeout=30000)
                try:
                    self.page.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass
                current = self.get_package_balance(locator)
                if current != balance_before:
                    return
        else:
            self.page.reload(timeout=30000)
            try:
                self.page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass

    def add_tokens_and_get_toast(self, locator, amount, comment):
        """Добавляет токены и возвращает текст toast-уведомления."""
        self.page.locator(locator.ADD_TOKENS_BTN).click()
        self.page.locator(locator.TOKEN_AMOUNT_INPUT).wait_for(
            state="visible", timeout=10000
        )
        amount_el = self.page.locator(locator.TOKEN_AMOUNT_INPUT)
        amount_el.click()
        amount_el.fill(amount)
        amount_el.evaluate("""el => {
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }""")
        comment_el = self.page.locator(locator.TOKEN_COMMENT_INPUT)
        comment_el.click()
        comment_el.fill(comment)
        comment_el.evaluate("""el => {
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }""")
        self.page.wait_for_timeout(500)
        self.page.locator(locator.TOKEN_SAVE_BTN).click()
        # Ждём появления toast-уведомления
        self.page.locator(locator.TOAST_BODY).wait_for(
            state="visible", timeout=10000
        )
        return self.page.locator(locator.TOAST_BODY).inner_text()

    def select_paid_plan(self, locator, plan_btn_locator):
        """Подключает платный тариф: клик → 'Уверен' → 'Отлично' → возврат на биллинг.

        Args:
            locator: объект с общими локаторами (CONFIRM_BTN, SUCCESS_BTN)
            plan_btn_locator: CSS-селектор кнопки 'Подключить' конкретного тарифа
        """
        # nth(0) — первая кнопка (платный раздел)
        self.page.locator(plan_btn_locator).nth(0).click()
        self.page.locator(locator.CONFIRM_BTN).wait_for(
            state="visible", timeout=10000
        )
        self.page.locator(locator.CONFIRM_BTN).click()
        self.page.locator(locator.SUCCESS_BTN).wait_for(
            state="visible", timeout=10000
        )
        self.page.locator(locator.SUCCESS_BTN).click()
        self.page.wait_for_url("**/settings-company/billing**", timeout=15000)
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass

    def get_invoice_status(self, locator):
        """Кликает вкладку 'Счета' и возвращает текст статуса первого счёта."""
        self.page.locator(locator.INVOICES_TAB).click()
        self.page.wait_for_timeout(2000)
        self.page.locator(locator.INVOICE_STATUS).wait_for(
            state="visible", timeout=10000
        )
        return self.page.locator(locator.INVOICE_STATUS).inner_text()

    def add_bank_account(self, locator, org_query):
        """Добавляет платёжную информацию (расчётный счёт) через автодополнение.

        Открывает форму, вводит название организации, выбирает первую подсказку
        (ИНН, ОГРН, адрес заполняются автоматически), сохраняет.
        """
        self.page.locator(locator.ADD_PAYMENT_BTN).click()
        self.page.wait_for_timeout(2000)
        self.page.locator(locator.BANK_ACCOUNT_TAB).click()
        self.page.wait_for_timeout(2000)
        # Вводим название организации
        name_input = self.page.locator(locator.ORG_NAME_INPUT)
        name_input.click()
        name_input.fill(org_query)
        name_input.evaluate(
            "el => el.dispatchEvent(new Event('input', { bubbles: true }))"
        )
        # Ждём появления подсказок и кликаем первую
        self.page.locator(locator.FIRST_SUGGESTION).first.wait_for(
            state="visible", timeout=10000
        )
        self.page.locator(locator.FIRST_SUGGESTION).first.click()
        self.page.wait_for_timeout(1000)
        # Сохраняем
        self.page.locator(locator.SAVE_PAYMENT_BTN).click()
        self.page.locator(locator.TOAST_BODY).wait_for(
            state="visible", timeout=10000
        )

    def get_payment_info_text(self, locator):
        """Возвращает текст секции 'Платёжная информация'."""
        self.page.locator(locator.PAYMENT_INFO_SECTION).wait_for(
            state="visible", timeout=10000
        )
        return self.page.locator(locator.PAYMENT_INFO_SECTION).inner_text()

    def get_current_plan_name(self, locator, expected_plan=None, base_url=None, client_id=None):
        """Возвращает текст текущего тарифа на странице биллинга.

        Если передан expected_plan — повторяет проверку до 10 раз с перезагрузкой,
        ожидая, пока план применится на бэкенде.
        """
        if expected_plan and base_url and client_id:
            billing_url = f"{base_url}/settings-company/billing?client_id={client_id}"
            for _ in range(10):
                try:
                    title = self.page.locator(locator.CURRENT_PLAN_TITLE).inner_text(
                        timeout=5000
                    )
                    if expected_plan in title:
                        return title
                except Exception:
                    pass
                self.page.wait_for_timeout(3000)
                self.page.goto(billing_url, timeout=30000)
                try:
                    self.page.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass
        self.page.locator(locator.CURRENT_PLAN_TITLE).wait_for(
            state="visible", timeout=10000
        )
        return self.page.locator(locator.CURRENT_PLAN_TITLE).inner_text()
