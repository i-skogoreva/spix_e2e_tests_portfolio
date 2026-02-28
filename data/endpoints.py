class Endpoints:
    AUTHORIZATION_USER_ENDPOINT = "/signin/"
    FEEDBACK_PAGE_ENDPOINT = "/1?feedbacks_tab=pending"
    SUPPORT_SIGNIN_ENDPOINT = "/support-signin"
    PASS_RECOVERY_ENDPOINT = "/pass-recovery"
    PASS_RECOVERY_SEND_ENDPOINT = "/pass-recovery-send"
    CLIENTS_ENDPOINT = "/clients"          # используется старыми фикстурами
    SUPPORT_PAGE_ENDPOINT = "/support"
    PROFILE_PAGE_ENDPOINT = "/profile"
    INSTRUCTIONS_URL = "https://spix.ru/instructions/"
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
    STATISTIC_MONTH_ENDPOINT = "/statistic/month"
    # Базовый URL страницы статистики (для fresh-пользователей без истории /statistic/month
    # редиректит на /statistic, поэтому проверяем наличие /statistic в URL)
    STATISTIC_ENDPOINT = "/statistic"

    # ── REST API ──────────────────────────────────────────────────────────
    BASE_URL = "https://go.dev.spix.ru"
    API_PREFIX = "abc8db6ftXiaLdstybcfia7eftDo5ByfJabksduy6fba7sdbtfka"
    API_CLIENTS = f"/{API_PREFIX}/clients/"
    API_CLIENTS_LIST = f"/{API_PREFIX}/clients-list/0"   # полный список с billing + users
    API_ACCOUNTS = f"/{API_PREFIX}/accounts/"            # + {client_id}/
    API_BILLING_INFO = f"/{API_PREFIX}/clients/"         # + {client_id}/billing-info
    API_USERS_ME = f"/{API_PREFIX}/users/me"
    API_USERS = f"/{API_PREFIX}/users/"                  # + {user_id} или POST для создания
    # object_type_id в ответе /accounts/{client_id}/
    SOURCE_TYPE_MARKETPLACES = 1   # Маркетплейсы
    SOURCE_TYPE_CARDS = 3          # Карты

    # language_id в профиле пользователя
    LANGUAGE_ID_RU = 1   # Русский
    LANGUAGE_ID_EN = 2   # English
    LANGUAGE_ID_ID = 3   # Indonesia

    # billing_plan_name допустимых значений для тарифа ≥ ПРО
    # Сравнение регистронезависимое: приводим к верхнему регистру перед проверкой
    BILLING_PLANS_PRO_AND_ABOVE = {"ПРО", "БИЗНЕС", "УЛЬТРА"}
