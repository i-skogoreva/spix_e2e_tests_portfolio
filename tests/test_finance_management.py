import allure

from locators.finance_management_locators import FinanceManagementLocators
from pages.finance_management_page import FinanceManagementPage
from data.dataclasses.finance_management_dataclass import FinanceManagementData
from data.endpoints import Endpoints
from utils.assertions.assertions import Assertions


@allure.feature("Управление финансами")
@allure.story("Биллинг")
class TestFinanceManagement:
    locator = FinanceManagementLocators()
    data = FinanceManagementData()
    endpoints = Endpoints()
    assertion = Assertions()

    @allure.title("TC-0401s: Субадмин подключает пробный бесплатный тариф ПРО")
    @allure.description(
        "Субадмин создаёт клиента (Демо-тариф), переходит в раздел Финансы, "
        "подключает пробный бесплатный тариф ПРО и проверяет, "
        "что тариф ПРО отображается на странице биллинга."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0401s_connect_free_pro_trial(self, demo_subadmin_page, demo_client):
        finance_page = FinanceManagementPage(demo_subadmin_page)

        with allure.step("Открыть страницу биллинга для demo-клиента"):
            finance_page.open_billing_for_client(
                self.endpoints.BASE_URL,
                demo_client["id"],
                upgrade_locator=self.locator.UPGRADE_BTN,
            )

        with allure.step("Нажать кнопку 'Улучшить'"):
            finance_page.click_upgrade(self.locator)

        with allure.step("Выбрать бесплатный пробный тариф ПРО и подтвердить"):
            finance_page.select_free_plan(self.locator, self.locator.PRO_PLAN_CONNECT_BTN)

        with allure.step("Проверить, что текущий тариф содержит 'ПРО'"):
            plan_name = finance_page.get_current_plan_name(
                self.locator,
                expected_plan=self.data.PRO_TRIAL_PLAN_NAME,
                base_url=self.endpoints.BASE_URL,
                client_id=demo_client["id"],
            )
            self.assertion.assert_true(
                self.data.PRO_TRIAL_PLAN_NAME in plan_name,
                f"Тариф ПРО не отображается. Текущий тариф: '{plan_name}'"
            )

    @allure.title("TC-0402s: Смена на другой бесплатный тариф")
    @allure.description(
        "У клиента уже подключён пробный тариф ПРО (после TC-0401s). "
        "Субадмин переходит в раздел Финансы, меняет тариф на БИЗНЕС (пробный) "
        "и проверяет, что тариф БИЗНЕС отображается на странице биллинга."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0402s_switch_to_another_free_plan(self, demo_subadmin_page, demo_client):
        finance_page = FinanceManagementPage(demo_subadmin_page)

        with allure.step("Открыть страницу биллинга для demo-клиента"):
            finance_page.open_billing_for_client(
                self.endpoints.BASE_URL,
                demo_client["id"],
                upgrade_locator=self.locator.UPGRADE_BTN,
            )

        with allure.step("Нажать кнопку 'Улучшить'"):
            finance_page.click_upgrade(self.locator)

        with allure.step("Выбрать бесплатный пробный тариф БИЗНЕС и подтвердить"):
            finance_page.select_free_plan(self.locator, self.locator.BUSINESS_PLAN_CONNECT_BTN)

        with allure.step("Проверить, что текущий тариф содержит 'БИЗНЕС'"):
            plan_name = finance_page.get_current_plan_name(
                self.locator,
                expected_plan=self.data.BUSINESS_TRIAL_PLAN_NAME,
                base_url=self.endpoints.BASE_URL,
                client_id=demo_client["id"],
            )
            self.assertion.assert_true(
                self.data.BUSINESS_TRIAL_PLAN_NAME in plan_name,
                f"Тариф БИЗНЕС не отображается. Текущий тариф: '{plan_name}'"
            )

    @allure.title("TC-0403s: Добавление токенов")
    @allure.description(
        "У клиента подключён тариф БИЗНЕС (после TC-0402s). "
        "Субадмин нажимает 'Добавить токены на период', вводит количество "
        "и комментарий, подтверждает. Проверяет, что остаток пакета увеличился."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0403s_add_tokens(self, demo_subadmin_page, demo_client):
        finance_page = FinanceManagementPage(demo_subadmin_page)

        with allure.step("Открыть страницу биллинга для demo-клиента"):
            finance_page.open_billing_for_client(
                self.endpoints.BASE_URL,
                demo_client["id"],
                upgrade_locator=self.locator.UPGRADE_BTN,
            )

        with allure.step("Запомнить текущий остаток токенов"):
            balance_before = finance_page.get_package_balance(self.locator)

        with allure.step("Добавить токены на период"):
            finance_page.add_tokens(
                self.locator,
                self.data.TOKEN_AMOUNT,
                self.data.TOKEN_COMMENT,
                base_url=self.endpoints.BASE_URL,
                client_id=demo_client["id"],
                balance_before=balance_before,
            )

        with allure.step("Проверить, что остаток пакета увеличился"):
            balance_after = finance_page.get_package_balance(self.locator)
            expected = balance_before + int(self.data.TOKEN_AMOUNT)
            self.assertion.assert_true(
                balance_after == expected,
                f"Остаток токенов не совпадает. "
                f"Было: {balance_before}, добавили: {self.data.TOKEN_AMOUNT}, "
                f"ожидали: {expected}, получили: {balance_after}"
            )

    @allure.title("TC-0404s: Появление уведомления о добавлении токенов")
    @allure.description(
        "Субадмин добавляет токены на период. "
        "После сохранения появляется toast-уведомление 'Токены успешно добавлены'."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_tc_0404s_token_success_notification(self, demo_subadmin_page, demo_client):
        finance_page = FinanceManagementPage(demo_subadmin_page)

        with allure.step("Открыть страницу биллинга для demo-клиента"):
            finance_page.open_billing_for_client(
                self.endpoints.BASE_URL,
                demo_client["id"],
                upgrade_locator=self.locator.UPGRADE_BTN,
            )

        with allure.step("Добавить токены и получить текст уведомления"):
            toast_text = finance_page.add_tokens_and_get_toast(
                self.locator,
                self.data.TOKEN_AMOUNT,
                self.data.TOKEN_COMMENT,
            )

        with allure.step("Проверить текст уведомления"):
            self.assertion.assert_true(
                self.data.TOKEN_SUCCESS_TOAST in toast_text,
                f"Ожидали уведомление '{self.data.TOKEN_SUCCESS_TOAST}', "
                f"получили: '{toast_text}'"
            )

    @allure.title("TC-0405s: Проверка выставления счёта при подключении платного тарифа")
    @allure.description(
        "Субадмин подключает платный тариф ПРО. "
        "После подтверждения на странице биллинга во вкладке 'Счета' "
        "появляется счёт со статусом 'Ожидает оплаты'."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0405s_paid_plan_invoice(self, demo_subadmin_page, demo_client):
        finance_page = FinanceManagementPage(demo_subadmin_page)

        with allure.step("Открыть страницу биллинга для demo-клиента"):
            finance_page.open_billing_for_client(
                self.endpoints.BASE_URL,
                demo_client["id"],
                upgrade_locator=self.locator.UPGRADE_BTN,
            )

        with allure.step("Нажать кнопку 'Улучшить'"):
            finance_page.click_upgrade(self.locator)

        with allure.step("Выбрать платный тариф ПРО и подтвердить"):
            finance_page.select_paid_plan(self.locator, self.locator.PRO_PLAN_CONNECT_BTN)

        with allure.step("Проверить, что на вкладке 'Счета' появился счёт 'Ожидает оплаты'"):
            invoice_status = finance_page.get_invoice_status(self.locator)
            self.assertion.assert_true(
                self.data.INVOICE_STATUS_PENDING in invoice_status,
                f"Счёт не найден или статус не совпадает. "
                f"Ожидали: '{self.data.INVOICE_STATUS_PENDING}', "
                f"получили: '{invoice_status}'"
            )

    @allure.title("TC-0406s: Добавление платёжной информации: расчётный счёт")
    @allure.description(
        "Субадмин открывает форму платёжной информации, выбирает 'Рас. счет', "
        "вводит название организации, выбирает из автодополнения, сохраняет. "
        "Проверяет, что в секции 'Платёжная информация' отображается 'Расчетный счет'."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tc_0406s_add_bank_account(self, demo_subadmin_page, demo_client):
        finance_page = FinanceManagementPage(demo_subadmin_page)

        with allure.step("Открыть страницу биллинга для demo-клиента"):
            finance_page.open_billing_for_client(
                self.endpoints.BASE_URL,
                demo_client["id"],
                upgrade_locator=self.locator.UPGRADE_BTN,
            )

        with allure.step("Добавить расчётный счёт через автодополнение"):
            finance_page.add_bank_account(
                self.locator,
                self.data.ORG_SEARCH_QUERY,
            )

        with allure.step("Проверить, что платёжная информация содержит 'Расчетный счет'"):
            payment_text = finance_page.get_payment_info_text(self.locator)
            self.assertion.assert_true(
                self.data.EXPECTED_PAYMENT_METHOD in payment_text,
                f"Платёжная информация не содержит '{self.data.EXPECTED_PAYMENT_METHOD}'. "
                f"Текст секции: '{payment_text}'"
            )

