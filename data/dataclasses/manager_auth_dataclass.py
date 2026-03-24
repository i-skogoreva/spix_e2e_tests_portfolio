from faker import Faker

fake = Faker()


class ManagerAuthData:
    MANAGER_PASSWORD = "Qwerty123"

    def __init__(self):
        self.CLIENT_NAME = f"Автотест_{fake.word()}_{fake.random_int(0, 9999)}"
        self.CLIENT_EMAIL = f"autotest_{fake.random_int(0, 99999)}@spix.im"
        self.MANAGER_NAME = f"Менеджер_{fake.word()}"
        self.MANAGER_PHONE = f"+7000{fake.random_int(1000000, 9999999)}"
        self.MANAGER_EMAIL = f"manager_{fake.random_int(0, 99999)}@spix.im"
