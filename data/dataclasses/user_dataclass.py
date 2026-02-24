from dotenv import load_dotenv
import os

load_dotenv()

class UserData:
    BASE_URL = "https://go.dev.spix.ru"
    SUBADMIN_PHONE_NUMBER = os.getenv("SUBADMIN_PHONE_NUMBER")
    SUBADMIN_PASSWORD = os.getenv("SUBADMIN_PASSWORD")
    MANAGER_PHONE_NUMBER = os.getenv("MANAGER_PHONE_NUMBER")
    MANAGER_PASSWORD = os.getenv("MANAGER_PASSWORD")
    OPERATOR_PHONE_NUMBER = os.getenv("OPERATOR_PHONE_NUMBER")
    OPERATOR_PASSWORD = os.getenv("OPERATOR_PASSWORD")
    SMS_CODE = "123456"
    WRONG_PASSWORD = "WrongPassword123!"
    WRONG_PHONE_NUMBER = "+7 0001112233"
    ERROR_MESSAGE_PASSWORD = "Incorrect username or password"
    KAZAKHSTAN_PHONE_PLACEHOLDER = "+7 771 000 9998"
    KAZAKHSTAN_FLAG_CLASS = "vti__flag kz"

    LANG_TRANSLATIONS = {
        "English": {
            "title": "Sign in",
            "description": "Enter your phone and password to log in",
            "phone_label": "Phone number",
            "password_label": "Password",
            "recover_pass": "Recover password",
        },
        "Indonesia": {
            "title": "Masuk",
            "description": "Masukkan nomor ponsel dan kata sandi Anda untuk masuk",
            "phone_label": "Nomor telepon",
            "password_label": "Kata sandi",
            "recover_pass": "Pulihkan kata sandi",
        },
        "Русский": {
            "title": "Авторизация",
            "description": "Введите телефон и пароль, чтобы войти в систему",
            "phone_label": "Телефон",
            "password_label": "Пароль",
            "recover_pass": "Восстановить пароль",
        },
    }
