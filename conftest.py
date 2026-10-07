import uuid
from urllib.parse import urlparse, parse_qs
import pytest
from playwright.sync_api import Playwright, ViewportSize
from locators.authorization_locators import UserAuthorization
from locators.clients_page_locators import ClientsPageLocators
from locators.profile_locators import ProfileLocators
from data.dataclasses.user_dataclass import UserData
from data.dataclasses.manager_auth_dataclass import ManagerAuthData
from data.dataclasses.finance_management_dataclass import FinanceManagementData
from pages.authorization_page import UserAuthorizationPage
from pages.clients_page import ClientsPage
from data.endpoints import Endpoints

data = UserData()
user_authorization = UserAuthorization()
clients_locator = ClientsPageLocators()
endpoint = Endpoints()

@pytest.fixture()
def page(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(ignore_https_errors=True, 
        viewport=ViewportSize(width=1440, height=980),
        base_url=f"{Endpoints.BASE_URL}/"
    )
    page = context.new_page()
    yield page
    page.wait_for_timeout(3000)
    page.close()
    context.close()
    browser.close()

@pytest.fixture(scope="session")
def get_cookies(playwright: Playwright):
    phone_number = data.PHONE_NUMBER
    password = data.PASSWORD
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        ignore_https_errors=True,
        base_url=f"{Endpoints.BASE_URL}/"
    )
    page = context.new_page()
    page.goto('/')
    page.locator(user_authorization.PHONE_FIELD_LOC).fill(phone_number)
    page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(password)
    page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
    page.wait_for_timeout(2000)
    cookies = context.cookies()
    page.close()
    context.close()
    browser.close()
    return cookies


@pytest.fixture()
def authorized_user(playwright: Playwright, get_cookies):
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(ignore_https_errors=True, 
        viewport=ViewportSize(width=1440, height=980),
        base_url=f"{Endpoints.BASE_URL}/"
    )
    context.add_cookies(get_cookies)
    page = context.new_page()
    yield page
    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope="session")
def subadmin_context(playwright: Playwright):
    """Авторизует субадмина один раз и хранит контекст на всю сессию"""
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(ignore_https_errors=True, 
        viewport=ViewportSize(width=1440, height=980),
        base_url=f"{Endpoints.BASE_URL}/"
    )
    page = context.new_page()
    page.goto("/", timeout=60000)
    page.locator(user_authorization.PHONE_FIELD_LOC).fill(data.SUBADMIN_PHONE_NUMBER)
    page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(data.SUBADMIN_PASSWORD)
    page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
    page.wait_for_url("**/1?**")
    page.close()

    # Гарантируем русский язык интерфейса перед запуском тестов
    ep = Endpoints()
    me_resp = context.request.get(f"{ep.BASE_URL}{ep.API_USERS_ME}")
    user = me_resp.json()["user"]
    if user.get("language_id") != ep.LANGUAGE_ID_RU:
        context.request.put(
            f"{ep.BASE_URL}{ep.API_USERS}{user['id']}",
            data={
                "nm": user["nm"],
                "email": user["email"],
                "has_marketing_consent": user.get("has_marketing_consent", 0),
                "language_id": ep.LANGUAGE_ID_RU,
            }
        )

    yield context
    context.close()
    browser.close()


@pytest.fixture()
def subadmin_page(subadmin_context, auto_client):
    """Создаёт новую страницу в уже авторизованном контексте субадмина.

    Зависит от auto_client, чтобы тестовый клиент был создан до первого теста.
    Если сессия истекла,
    выполняет повторную авторизацию перед созданием страницы.
    """
    ep = Endpoints()
    session_ok = False
    try:
        me_resp = subadmin_context.request.get(f"{ep.BASE_URL}{ep.API_USERS_ME}")
        resp_data = me_resp.json()
        session_ok = isinstance(resp_data, dict) and resp_data.get("user") is not None
    except Exception:
        session_ok = False

    page = subadmin_context.new_page()
    if not session_ok:
        # Сессия истекла — повторная авторизация
        page.goto("/", timeout=60000)
        page.locator(user_authorization.PHONE_FIELD_LOC).fill(data.SUBADMIN_PHONE_NUMBER)
        page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(data.SUBADMIN_PASSWORD)
        page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
        page.wait_for_url("**/1?**", timeout=30000)
        page.close()
        page = subadmin_context.new_page()

    yield page
    page.close()


@pytest.fixture(scope="session")
def auto_client(subadmin_context):
    """Создаёт тестового клиента через UI (тариф ПРО пробный + источники Fake и Fake Geo).

    Setup:
      1. Создаём клиента «Авто_<uid>» на странице /clients
      2. Получаем id через API /clients-list/0
      3. Переключаем тариф на ПРО (пробный) через страницу биллинга
      4. Добавляем источник Маркетплейсы → Fake (10 товаров / 100 отзывов в час)
      5. Добавляем источник Карты → Fake Geo (10 товаров / 100 отзывов в час)

    Teardown: удаляет клиента через API DELETE после завершения всех тестов сьюта.
    """
    ep = Endpoints()
    base = ep.BASE_URL
    client_nm = "TestClient"
    client_email = "auto@example.com"
    page = subadmin_context.new_page()

    # ── 1. Создаём клиента — кнопка "+" на странице Клиенты ──────────────
    page.goto(f"{base}{ep.CLIENTS_PAGE_ENDPOINT}", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=15000)
    page.locator(".sticky-btns-container button").last.click(timeout=10000)
    page.locator("input[placeholder='Введите название клиента']").wait_for(state="visible", timeout=10000)
    page.locator("input[placeholder='Введите название клиента']").fill(client_nm)
    page.locator("input[placeholder='Введите email клиента']").fill(client_email)
    page.locator("button:has-text('Добавить')").click()
    page.wait_for_timeout(3000)

    # ── 2. Получаем ID созданного клиента через API ───────────────────────
    clients_resp = subadmin_context.request.get(f"{base}{ep.API_CLIENTS_LIST}")
    all_clients = clients_resp.json()
    if isinstance(all_clients, dict):
        all_clients = all_clients.get("clients", [])
    client_data = next((c for c in all_clients if c.get("nm") == client_nm), None)
    assert client_data, f"Клиент {client_nm!r} не найден в ответе API"
    client_id = client_data["id"]

    # ── 3. Биллинг: ждём Демо-план, затем переключаем на ПРО (пробный) ───
    for _ in range(8):
        page.goto(f"{base}/settings-company/billing?client_id={client_id}", timeout=30000)
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        try:
            page.locator(".billing-package__btn").wait_for(state="visible", timeout=5000)
            break
        except Exception:
            page.wait_for_timeout(5000)
    page.locator(".billing-package__btn").click()
    page.wait_for_url("**/billing-plan**", timeout=15000)
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    # Скроллим к разделу "Бесплатные тарифы для теста (7 дней)"
    page.locator("h2.billing-plan__title:has-text('Бесплатные тарифы')").scroll_into_view_if_needed()
    # nth(1) — вторая кнопка "Подключить" на карточке ПРО (первая — в платном разделе)
    page.locator(".card:has(.card__name:has-text('ПРО')) .card__button").nth(1).click()
    page.locator("button:has-text('Уверен')").wait_for(state="visible", timeout=10000)
    page.locator("button:has-text('Уверен')").click()
    page.locator("button:has-text('Отлично')").wait_for(state="visible", timeout=10000)
    page.locator("button:has-text('Отлично')").click()
    page.wait_for_url("**/settings-company/billing**", timeout=15000)
    page.wait_for_load_state("networkidle", timeout=10000)
    # Проверяем, что тариф ПРО (пробный) действительно присвоен.
    # Если план ещё не применился — перезагружаем страницу и повторяем.
    for _ in range(10):
        try:
            title = page.locator(".billing-package__col-title").inner_text(timeout=5000)
            if "ПРО" in title:
                break
        except Exception:
            pass
        page.wait_for_timeout(3000)
        page.goto(f"{base}/settings-company/billing?client_id={client_id}", timeout=30000)
        page.wait_for_load_state("networkidle", timeout=15000)
    else:
        raise RuntimeError(
            f"Тариф ПРО (пробный) не присвоился клиенту {client_id} после нескольких попыток"
        )

    # ── 4. Добавляем источник Маркетплейсы → Fake ─────────────────────────
    page.goto(f"{base}/settings/sources?client_id={client_id}", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=15000)
    page.locator("button.button-main:has-text('Добавить источник данных')").click()
    page.wait_for_url("**/add-source**", timeout=10000)
    page.locator(".add-source__object-type-name:has-text('Маркетплейсы')").click()
    page.locator(".add-source-options__option-nm:has-text('Fake')").first.click()
    page.wait_for_url("**/add-source/fk**", timeout=10000)
    page.wait_for_load_state("networkidle", timeout=10000)
    page.locator("input[placeholder='Кол-во товаров']").fill("10")
    page.locator("input[placeholder='Кол-во отзывов в час']").fill("100")
    page.locator("button:has-text('Добавить источник')").click()
    page.wait_for_load_state("networkidle", timeout=15000)
    page.locator("button:has-text('Завершить')").click()
    page.locator("button:has-text('Отлично')").wait_for(state="visible", timeout=10000)
    page.locator("button:has-text('Отлично')").click()

    # ── 5. Добавляем источник Карты → Fake Geo ────────────────────────────
    page.wait_for_load_state("networkidle", timeout=15000)
    page.locator(".sticky-btns-container button").last.click(timeout=10000)
    page.wait_for_url("**/add-source**", timeout=10000)
    page.locator(".add-source__object-type-name:has-text('Карты')").click()
    page.locator(".add-source-options__option-nm:has-text('Fake Geo')").first.click()
    page.wait_for_url("**/add-source/f**", timeout=10000)
    page.wait_for_load_state("networkidle", timeout=10000)
    page.locator("input[placeholder='Кол-во товаров']").fill("10")
    page.locator("input[placeholder='Кол-во отзывов в час']").fill("100")
    page.locator("button:has-text('Добавить источник')").click()
    page.wait_for_load_state("networkidle", timeout=15000)
    page.locator("button:has-text('Завершить')").click()
    page.locator("button:has-text('Отлично')").wait_for(state="visible", timeout=10000)
    page.locator("button:has-text('Отлично')").click()
    page.wait_for_load_state("networkidle", timeout=10000)
    page.close()

    yield {"id": client_id, "nm": client_nm}

    # ── TEARDOWN: удаляем клиента через API ──────────────────────────────
    try:
        subadmin_context.request.delete(f"{base}{ep.API_CLIENTS}{client_id}/")
    except Exception:
        pass


@pytest.fixture(scope="session")
def demo_client(subadmin_context):
    """Создаёт клиента через UI БЕЗ смены тарифа (остаётся Демо).

    Setup:
      1. Создаём клиента на странице /clients
      2. Получаем id через API /clients-list/0

    Teardown: удаляет клиента через API DELETE.
    """
    ep = Endpoints()
    base = ep.BASE_URL
    fm_data = FinanceManagementData()
    client_nm = fm_data.CLIENT_NAME
    client_email = fm_data.CLIENT_EMAIL
    page = subadmin_context.new_page()

    # ── 1. Создаём клиента — кнопка "+" на странице Клиенты ──────────────
    page.goto(f"{base}{ep.CLIENTS_PAGE_ENDPOINT}", timeout=30000)
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    # Закрываем попап, если он появился
    try:
        page.locator("button:has-text('В другой раз')").click(timeout=3000)
        page.wait_for_timeout(300)
    except Exception:
        pass
    page.locator(".sticky-btns-container button").last.click(timeout=10000)
    page.locator("input[placeholder='Введите название клиента']").wait_for(
        state="visible", timeout=10000
    )
    page.locator("input[placeholder='Введите название клиента']").fill(client_nm)
    page.locator("input[placeholder='Введите email клиента']").fill(client_email)
    page.locator("button:has-text('Добавить')").click()
    page.wait_for_timeout(3000)

    # ── 2. Получаем ID созданного клиента через API ───────────────────────
    clients_resp = subadmin_context.request.get(f"{base}{ep.API_CLIENTS_LIST}")
    all_clients = clients_resp.json()
    if isinstance(all_clients, dict):
        all_clients = all_clients.get("clients", [])
    client_data = next((c for c in all_clients if c.get("nm") == client_nm), None)
    assert client_data, f"Клиент {client_nm!r} не найден в ответе API"
    client_id = client_data["id"]
    page.close()

    yield {"id": client_id, "nm": client_nm}

    # ── TEARDOWN: удаляем клиента через API ──────────────────────────────
    try:
        subadmin_context.request.delete(f"{base}{ep.API_CLIENTS}{client_id}/")
    except Exception:
        pass


@pytest.fixture()
def demo_subadmin_page(subadmin_context, demo_client):
    """Страница субадмина для тестов, НЕ зависящих от auto_client.

    Использует demo_client вместо auto_client. Логика восстановления
    сессии аналогична subadmin_page.
    """
    ep = Endpoints()
    session_ok = False
    try:
        me_resp = subadmin_context.request.get(f"{ep.BASE_URL}{ep.API_USERS_ME}")
        resp_data = me_resp.json()
        session_ok = isinstance(resp_data, dict) and resp_data.get("user") is not None
    except Exception:
        session_ok = False

    page = subadmin_context.new_page()
    if not session_ok:
        page.goto("/", timeout=60000)
        page.locator(user_authorization.PHONE_FIELD_LOC).fill(data.SUBADMIN_PHONE_NUMBER)
        page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(data.SUBADMIN_PASSWORD)
        page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
        page.wait_for_url("**/1?**", timeout=30000)
        page.close()
        page = subadmin_context.new_page()

    yield page
    page.close()


@pytest.fixture(scope="session")
def manager_user_setup(subadmin_context, auto_client):
    """Создаёт пользователя с ролью менеджер через API и возвращает его credentials.

    Генерирует уникальный телефон (+70001XXXXXX) и email (manager_XXXXXXXX@example.com)
    чтобы каждый запуск создавал нового пользователя без конфликтов.
    """
    ep = Endpoints()
    base = ep.BASE_URL

    uid      = uuid.uuid4()
    phone    = f"+70001{uid.int % 1000000:06d}"
    password = data.MANAGER_PASSWORD or "TestPass123!"
    email    = f"manager_{uid.hex[:8]}@example.com"

    resp = subadmin_context.request.post(
        f"{base}{ep.API_USERS}",
        data={
            "nm":            "Test Manager",
            "phone":         phone,
            "email":         email,
            "pass":          password,
            "role":          "manager",
            "client_id":     auto_client["id"],
            "telegram_nick": None,
        }
    )
    if resp.status not in (200, 201):
        raise RuntimeError(
            f"Не удалось создать менеджера: HTTP {resp.status}, "
            f"body={resp.text()[:300]}"
        )
    return {
        "phone":     phone,
        "password":  password,
        "client_nm": auto_client["nm"],
    }


@pytest.fixture(scope="session")
def manager_context(playwright: Playwright, manager_user_setup):
    """Авторизует менеджера один раз и хранит контекст на всю сессию."""
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(ignore_https_errors=True, 
        viewport=ViewportSize(width=1440, height=980),
        base_url=f"{Endpoints.BASE_URL}/"
    )
    page = context.new_page()
    page.goto("/", timeout=60000)
    page.locator(user_authorization.PHONE_FIELD_LOC).fill(manager_user_setup["phone"])
    page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(manager_user_setup["password"])
    page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
    page.wait_for_url("**/1?**")
    # Закрываем приветственный попап "Быть в курсе новостей и акций"
    try:
        page.locator("button:has-text('В другой раз')").click(timeout=5000)
        page.wait_for_timeout(500)
    except Exception:
        pass
    page.close()

    # Гарантируем русский язык интерфейса
    ep = Endpoints()
    me_resp = context.request.get(f"{ep.BASE_URL}{ep.API_USERS_ME}")
    user = me_resp.json()["user"]
    if user.get("language_id") != ep.LANGUAGE_ID_RU:
        context.request.put(
            f"{ep.BASE_URL}{ep.API_USERS}{user['id']}",
            data={
                "nm": user["nm"],
                "email": user["email"],
                "has_marketing_consent": user.get("has_marketing_consent", 0),
                "language_id": ep.LANGUAGE_ID_RU,
            }
        )

    yield context

    # Teardown: удаляем профиль менеджера на странице «Мой профиль»
    ep = Endpoints()
    profile_loc = ProfileLocators()
    try:
        cleanup_page = context.new_page()
        cleanup_page.goto("/profile")
        cleanup_page.wait_for_load_state("networkidle", timeout=10000)

        # Если сессия истекла, повторно авторизуемся
        if ep.AUTHORIZATION_USER_ENDPOINT.rstrip("/") in cleanup_page.url:
            cleanup_page.locator(user_authorization.PHONE_FIELD_LOC).fill(manager_user_setup["phone"])
            cleanup_page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(manager_user_setup["password"])
            cleanup_page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
            cleanup_page.wait_for_url("**/1?**", timeout=15000)
            cleanup_page.goto("/profile")
            cleanup_page.wait_for_load_state("networkidle", timeout=10000)

        # Нажимаем «Удалить аккаунт» и подтверждаем
        cleanup_page.locator(profile_loc.DELETE_ACCOUNT_BTN).wait_for(state="visible", timeout=10000)
        cleanup_page.locator(profile_loc.DELETE_ACCOUNT_BTN).click()
        cleanup_page.locator(profile_loc.DELETE_CONFIRM_BTN).wait_for(state="visible", timeout=5000)
        cleanup_page.locator(profile_loc.DELETE_CONFIRM_BTN).click()
        cleanup_page.wait_for_timeout(2000)
        cleanup_page.close()
    except Exception:
        pass

    context.close()
    browser.close()


@pytest.fixture()
def manager_page(manager_context, manager_user_setup):
    """Создаёт новую страницу в уже авторизованном контексте менеджера.

    Если сессия истекла,
    выполняет повторную авторизацию перед созданием страницы.
    Проверка сессии: /users/me должен вернуть JSON с ключом 'user'.
    """
    ep = Endpoints()
    # Надёжная проверка сессии через содержимое JSON-ответа
    session_ok = False
    try:
        me_resp = manager_context.request.get(f"{ep.BASE_URL}{ep.API_USERS_ME}")
        resp_data = me_resp.json()
        session_ok = isinstance(resp_data, dict) and resp_data.get("user") is not None
    except Exception:
        session_ok = False

    page = manager_context.new_page()
    if not session_ok:
        # Сессия истекла — повторная авторизация
        page.goto("/", timeout=60000)
        page.locator(user_authorization.PHONE_FIELD_LOC).fill(manager_user_setup["phone"])
        page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(manager_user_setup["password"])
        page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
        page.wait_for_url("**/1?**", timeout=15000)
        page.wait_for_timeout(2000)
        try:
            page.locator("button:has-text('В другой раз')").click(timeout=3000)
            page.wait_for_timeout(500)
        except Exception:
            pass
        page.close()
        page = manager_context.new_page()
    yield page
    page.close()


# ══════════════════════════════════════════════════════════════════════════════
# Фикстуры для роли Оператор
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def operator_user_setup(subadmin_context, auto_client):
    """Создаёт пользователя с ролью operator через API и возвращает его credentials.

    Генерирует уникальный телефон (+70002XXXXXX) и email (operator_XXXXXXXX@example.com).
    Префикс +70002 отличается от менеджерского +70001 для исключения коллизий.
    """
    ep = Endpoints()
    base = ep.BASE_URL

    uid      = uuid.uuid4()
    phone    = f"+70002{uid.int % 1000000:06d}"
    password = data.OPERATOR_PASSWORD or "TestPass123!"
    email    = f"operator_{uid.hex[:8]}@example.com"

    resp = subadmin_context.request.post(
        f"{base}{ep.API_USERS}",
        data={
            "nm":            "Test Operator",
            "phone":         phone,
            "email":         email,
            "pass":          password,
            "role":          "operator",
            "client_id":     auto_client["id"],
            "telegram_nick": None,
        }
    )
    if resp.status not in (200, 201):
        raise RuntimeError(
            f"Не удалось создать оператора: HTTP {resp.status}, "
            f"body={resp.text()[:300]}"
        )
    return {
        "phone":     phone,
        "password":  password,
        "client_id": auto_client["id"],
        "client_nm": auto_client["nm"],
    }


@pytest.fixture(scope="session")
def operator_context(playwright: Playwright, operator_user_setup):
    """Авторизует оператора один раз и хранит контекст на всю сессию.

    После логина оператор попадает на страницу Отзывов (как менеджер, URL **/1?**).
    Закрывает попап «Быть в курсе новостей и акций». Устанавливает язык RU.
    """
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(ignore_https_errors=True, 
        viewport=ViewportSize(width=1440, height=980),
        base_url=f"{Endpoints.BASE_URL}/"
    )
    page = context.new_page()
    page.goto("/", timeout=60000)
    page.locator(user_authorization.PHONE_FIELD_LOC).fill(operator_user_setup["phone"])
    page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(operator_user_setup["password"])
    page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
    page.wait_for_url("**/1?**", timeout=30000)
    # Закрываем приветственный попап «Быть в курсе новостей и акций»
    try:
        page.locator("button:has-text('В другой раз')").click(timeout=5000)
        page.wait_for_timeout(500)
    except Exception:
        pass
    page.close()

    # Гарантируем русский язык интерфейса
    ep = Endpoints()
    me_resp = context.request.get(f"{ep.BASE_URL}{ep.API_USERS_ME}")
    user = me_resp.json()["user"]
    if user.get("language_id") != ep.LANGUAGE_ID_RU:
        context.request.put(
            f"{ep.BASE_URL}{ep.API_USERS}{user['id']}",
            data={
                "nm": user["nm"],
                "email": user["email"],
                "has_marketing_consent": user.get("has_marketing_consent", 0),
                "language_id": ep.LANGUAGE_ID_RU,
            }
        )

    yield context

    # Teardown: удаляем профиль оператора на странице «Мой профиль»
    ep = Endpoints()
    profile_loc = ProfileLocators()
    try:
        cleanup_page = context.new_page()
        cleanup_page.goto("/profile")
        cleanup_page.wait_for_load_state("networkidle", timeout=10000)

        # Если сессия истекла — повторно авторизуемся
        if ep.AUTHORIZATION_USER_ENDPOINT.rstrip("/") in cleanup_page.url:
            cleanup_page.locator(user_authorization.PHONE_FIELD_LOC).fill(operator_user_setup["phone"])
            cleanup_page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(operator_user_setup["password"])
            cleanup_page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
            cleanup_page.wait_for_url("**/1?**", timeout=30000)
            cleanup_page.goto("/profile")
            cleanup_page.wait_for_load_state("networkidle", timeout=10000)

        # Нажимаем «Удалить аккаунт» и подтверждаем
        cleanup_page.locator(profile_loc.DELETE_ACCOUNT_BTN).wait_for(state="visible", timeout=10000)
        cleanup_page.locator(profile_loc.DELETE_ACCOUNT_BTN).click()
        cleanup_page.locator(profile_loc.DELETE_CONFIRM_BTN).wait_for(state="visible", timeout=5000)
        cleanup_page.locator(profile_loc.DELETE_CONFIRM_BTN).click()
        cleanup_page.wait_for_timeout(2000)
        cleanup_page.close()
    except Exception:
        pass

    context.close()
    browser.close()


@pytest.fixture()
def operator_page(operator_context, operator_user_setup):
    """Создаёт новую страницу в уже авторизованном контексте оператора.

    Если сессия истекла,
    выполняет повторную авторизацию перед созданием страницы.
    """
    ep = Endpoints()
    session_ok = False
    try:
        me_resp = operator_context.request.get(f"{ep.BASE_URL}{ep.API_USERS_ME}")
        resp_data = me_resp.json()
        session_ok = isinstance(resp_data, dict) and resp_data.get("user") is not None
    except Exception:
        session_ok = False

    page = operator_context.new_page()
    if not session_ok:
        # Сессия предположительно истекла — проверяем по URL после перехода
        page.goto("/", timeout=60000)
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass
        # Если редиректнуло не на страницу логина — сессия жива, переавторизация не нужна
        if ep.AUTHORIZATION_USER_ENDPOINT.rstrip("/") not in page.url:
            yield page
            page.close()
            return
        page.locator(user_authorization.PHONE_FIELD_LOC).fill(operator_user_setup["phone"])
        page.locator(user_authorization.PASSWORD_FIELD_LOC).fill(operator_user_setup["password"])
        page.locator(user_authorization.SUBMIT_BUTTON_LOC).click()
        page.wait_for_url("**/1?**", timeout=30000)
        page.wait_for_timeout(2000)
        try:
            page.locator("button:has-text('В другой раз')").click(timeout=3000)
            page.wait_for_timeout(500)
        except Exception:
            pass
        page.close()
        page = operator_context.new_page()
    yield page
    page.close()


@pytest.fixture()
def client_page(playwright: Playwright):
    """Авторизуется под субадмином, создаёт клиента, переходит к форме добавления пользователя.

    Teardown: удаляет созданного клиента через API DELETE.
    """
    manager_data = ManagerAuthData()
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    context = browser.new_context(ignore_https_errors=True,
        viewport=ViewportSize(width=1440, height=980),
        base_url=f"{Endpoints.BASE_URL}/"
    )
    page = context.new_page()

    full_url = data.BASE_URL + endpoint.AUTHORIZATION_USER_ENDPOINT
    auth_page = UserAuthorizationPage(page, full_url)
    auth_page.open()
    auth_page.authorization_user_wildcard(
        user_authorization,
        data.SUBADMIN_PHONE_NUMBER,
        data.SUBADMIN_PASSWORD
    )

    clients_url = data.BASE_URL + endpoint.CLIENTS_ENDPOINT
    clients_page = ClientsPage(page, clients_url)
    clients_page.open()
    clients_page.wait_locator(clients_locator.ADD_CLIENT_BTN)

    clients_page.create_client(
        clients_locator,
        manager_data.CLIENT_NAME,
        manager_data.CLIENT_EMAIL
    )

    clients_page.click_first_client(manager_data.CLIENT_NAME)

    # Извлекаем client_id из URL (формат: ?client_id=XX)
    parsed = urlparse(page.url)
    qs = parse_qs(parsed.query)
    client_id = qs.get("client_id", [None])[0]

    clients_page.navigate_to_add_user(clients_locator)

    yield page

    # Teardown: удаляем клиента через API
    if client_id:
        try:
            ep = Endpoints()
            context.request.delete(f"{ep.BASE_URL}{ep.API_CLIENTS}{client_id}/")
        except Exception:
            pass

    page.wait_for_timeout(3000)
    page.close()
    context.close()
    browser.close()


