from faker import Faker

fake = Faker()


class OperatorAuthData:
    OPERATOR_NAME = f"Оператор_{fake.word()}"
    OPERATOR_PHONE = f"+7000{fake.random_int(1000000, 9999999)}"
    OPERATOR_EMAIL = f"operator_{fake.random_int(0, 99999)}@spix.im"
    OPERATOR_PASSWORD = "Qwerty123"
