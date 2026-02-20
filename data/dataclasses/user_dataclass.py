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
    CLIENT_LAYKOVY = "Лайковый клиент"
