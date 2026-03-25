from faker import Faker

fake = Faker()


class FinanceManagementData:
    CLIENT_NAME = f"Финансы_{fake.word()}_{fake.random_int(0, 9999)}"
    CLIENT_EMAIL = f"finance_{fake.random_int(0, 99999)}@spix.im"
    PRO_TRIAL_PLAN_NAME = "ПРО"
    BUSINESS_TRIAL_PLAN_NAME = "Бизнес"
    TOKEN_AMOUNT = "100"
    TOKEN_COMMENT = "Токены для инсайтов"
    TOKEN_SUCCESS_TOAST = "Токены успешно добавлены"
    INVOICE_STATUS_PENDING = "Ожидает оплаты"
    ORG_SEARCH_QUERY = "Сбербанк"
    EXPECTED_PAYMENT_METHOD = "Расчетный счет"
    PAYMENT_UPDATED_TOAST = "Платежная информация успешно обновлена"
