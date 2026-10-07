from faker import Faker

fake = Faker()


class FinanceManagementData:
    CLIENT_NAME = f"TestFinanceClient_{fake.word()}_{fake.random_int(0, 9999)}"
    CLIENT_EMAIL = f"finance_{fake.random_int(0, 99999)}@example.com"
    PRO_TRIAL_PLAN_NAME = "PRO"
    BUSINESS_TRIAL_PLAN_NAME = "Business"
    TOKEN_AMOUNT = "100"
    TOKEN_COMMENT = "Test tokens"
    TOKEN_SUCCESS_TOAST = "Токены успешно добавлены"
    INVOICE_STATUS_PENDING = "Ожидает оплаты"
    ORG_SEARCH_QUERY = "Test Company"
    EXPECTED_PAYMENT_METHOD = "Расчетный счет"
    PAYMENT_UPDATED_TOAST = "Платежная информация успешно обновлена"
