from faker import Faker

fake = Faker()


class OperatorAuthData:
    OPERATOR_NAME = f"TestOperator_{fake.word()}"
    OPERATOR_PHONE = f"+7000{fake.random_int(1000000, 9999999)}"
    OPERATOR_EMAIL = f"operator_{fake.random_int(0, 99999)}@example.com"
    OPERATOR_PASSWORD = "TestPassword123!"
