from faker import Faker

fake = Faker()


class ManagerAuthData:
    MANAGER_PASSWORD = "Qwerty123"

    SMS_PAGE_TRANSLATIONS = {
        "Русский": {
            "title": "Авторизация",
            "description": "Введите код из СМС",
            "code_label": "Код",
        },
        "English": {
            "title": "Sign in",
            "description": "Enter the code from SMS",
            "code_label": "Code",
        },
        "Indonesia": {
            "title": "Masuk",
            "description": "Masukkan kode dari SMS",
            "code_label": "Kode",
        },
    }

    def __init__(self):
        self.CLIENT_NAME = f"Автотест_{fake.word()}_{fake.random_int(0, 9999)}"
        self.CLIENT_EMAIL = f"autotest_{fake.random_int(0, 99999)}@spix.im"
        self.MANAGER_NAME = f"Менеджер_{fake.word()}"
        self.MANAGER_PHONE = f"+7000{fake.random_int(1000000, 9999999)}"
        self.MANAGER_EMAIL = f"manager_{fake.random_int(0, 99999)}@spix.im"
