from dotenv import load_dotenv
import os

load_dotenv()


class Endpoints:
    AUTHORIZATION_USER_ENDPOINT = "/signin/"
    FEEDBACK_PAGE_ENDPOINT = "/1?feedbacks_tab=pending"
    SUPPORT_SIGNIN_ENDPOINT = "/support-signin"
    PASS_RECOVERY_ENDPOINT = "/pass-recovery"
    PASS_RECOVERY_SEND_ENDPOINT = "/pass-recovery-send"
    CLIENTS_ENDPOINT = "/clients"
    SUPPORT_PAGE_ENDPOINT = "/support"
    PROFILE_PAGE_ENDPOINT = "/profile"
    INSTRUCTIONS_URL = "/instructions/"
    CHATS_PAGE_ENDPOINT = "/chats"
    PRODUCTS_PAGE_ENDPOINT = "/products"
    POIS_PAGE_ENDPOINT = "/pois"
    CLIENTS_PAGE_ENDPOINT = "/clients"
    HOME_POIS_ENDPOINT = "/home-pois"
    REVIEW_ANALYTICS_ENDPOINT = "/review-analytics"
    PROCESSING_ANALYTICS_ENDPOINT = "/processing-analytics"
    INSIGHTS_ENDPOINT = "/insights"
    COMPARISON_ANALYTICS_ENDPOINT = "/comparison-analytics"
    SETTINGS_PAGE_ENDPOINT = "/settings"
    SETTINGS_COMPANY_ENDPOINT = "/settings-company/settings"
    SETTINGS_COMPANY_USERS_ENDPOINT = "/settings-company/users"
    SETTINGS_COMPANY_BILLING_ENDPOINT = "/settings-company/billing"
    BRANDS_ENDPOINT = "/brands/"
    TEMPLATE_ANSWERS_ENDPOINT = "/settings/template-answers"
    STATISTIC_MONTH_ENDPOINT = "/statistic/month"
    STATISTIC_ENDPOINT = "/statistic"

    # REST API
    BASE_URL = os.getenv("BASE_URL", "https://example.com")
    API_PREFIX = "api"
    API_CLIENTS = f"/{API_PREFIX}/clients/"
    API_CLIENTS_LIST = f"/{API_PREFIX}/clients-list/0"
    API_ACCOUNTS = f"/{API_PREFIX}/accounts/"
    API_BILLING_INFO = f"/{API_PREFIX}/clients/"
    API_USERS_ME = f"/{API_PREFIX}/users/me"
    API_USERS = f"/{API_PREFIX}/users/"

    SOURCE_TYPE_MARKETPLACES = 1
    SOURCE_TYPE_CARDS = 3

    LANGUAGE_ID_RU = 1
    LANGUAGE_ID_EN = 2
    LANGUAGE_ID_ID = 3

    BILLING_PLANS_PRO_AND_ABOVE = {"PRO", "BUSINESS", "ENTERPRISE"}