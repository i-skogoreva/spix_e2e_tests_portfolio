class ClientsPageLocators:
    # Кнопка "+" для добавления клиента
    ADD_CLIENT_BTN = ".button-sticky"

    # Поля модалки создания клиента
    CLIENT_NAME_INPUT = "input[placeholder='Введите название клиента']"
    CLIENT_EMAIL_INPUT = "input[placeholder='Введите email клиента']"

    # Вкладка "Пользователи" на странице настроек клиента
    USERS_TAB = "text=Пользователи"

    # Кнопки быстрой навигации в строке клиента на странице /clients
    BTN_CLIENT_REVIEWS   = "button[aria-label='Смотреть отзывы клиента']"
    BTN_CLIENT_PRODUCTS  = "button[aria-label='Смотреть товары клиента']"
    BTN_CLIENT_MAPS      = "button[aria-label='Карты']"
    BTN_CLIENT_BRANDS    = "button[aria-label='Смотреть бренды клиента']"
    BTN_CLIENT_TEMPLATES = "button[aria-label='Смотреть группы шаблонных ответов клиента']"
    BTN_CLIENT_USERS     = "button[aria-label='Смотреть пользователей клиента']"
    BTN_CLIENT_SETTINGS  = ".item-cell.btns-group button:nth-child(8)"
    BTN_CLIENT_BILLING   = ".item-cell.btns-group button:nth-child(9)"