class SideMenuLocators:
    # Состояние бокового меню (открытое/широкое)
    SIDEBAR_OPEN = ".sidebar.with-sidebar"

    # Пункт меню Отзывы
    MENU_ITEM_REVIEWS = ".item__link-text:has-text('Отзывы')"

    # Активное подменю после раскрытия
    SUBMENU_ACTIVE = ".router-link-active.router-link-exact-active.item__link-text"

    # Пункт подменю Карты
    SUBMENU_ITEM_KARTY = ".item__link-text:has-text('Карты')"

    # Критерий 1: активный пункт подменю Карты (aria-current="page")
    KARTY_ARIA_CURRENT = "[aria-current='page']:has-text('Карты')"

    # Критерий 2: скелетон при загрузке страницы
    SKELETON = ".base-loader"

    # Пункт меню Чаты
    MENU_ITEM_CHATS = ".item__link-text:has-text('Чаты')"

    # Критерий 1: заголовок страницы чатов
    CHAT_PAGE_TITLE = ".chat-list__search-wrapper-title"

    # Критерий 2: боковое меню схлопнулось
    SIDEBAR_COLLAPSED = ".sidebar-wrapper.small"

    # Кнопка раскрытия/сворачивания бокового меню (burger)
    SIDEBAR_BURGER = ".burger.light"

    # Пункт меню Товары
    MENU_ITEM_PRODUCTS = ".item__link-text:has-text('Товары')"

    # Критерий: заголовок страницы Товары
    PRODUCTS_PAGE_TITLE = ".header__title:has-text('Товары')"

    # Пункт меню Места
    MENU_ITEM_PLACES = ".item__link-text:has-text('Места')"

    # Критерий: заголовок страницы Места
    PLACES_PAGE_TITLE = ".header__title:has-text('Места')"

    # Пункт меню Клиенты
    MENU_ITEM_CLIENTS = ".item__link-text:has-text('Клиенты')"

    # Критерий: заголовок страницы Клиенты
    CLIENTS_PAGE_TITLE = ".header__title:has-text('Клиенты')"

    # Пункт меню Аналитика
    MENU_ITEM_ANALYTICS = ".item__link-text:has-text('Аналитика')"

    # Критерий: подпункт Отзывы в подменю Аналитика
    ANALYTICS_SUBMENU_REVIEWS = ".item__link-text.is-inactive:has-text('Отзывы')"

    # Критерий 1: подпункт Отзывы активен после клика
    ANALYTICS_REVIEWS_ACTIVE = ".router-link-active.router-link-exact-active.item__link-text:has-text('Отзывы')"

    # Критерий 2: заголовок страницы Аналитика > Отзывы
    ANALYTICS_REVIEWS_PAGE_HEADER = ".analytics-section__header:has-text('Отзывы')"

    # Подпункт Обработка в подменю Аналитика (до клика — is-inactive)
    ANALYTICS_SUBMENU_PROCESSING = ".item__link-text.is-inactive:has-text('Обработка')"

    # Критерий 1: подпункт Обработка активен после клика
    ANALYTICS_PROCESSING_ACTIVE = ".router-link-active.router-link-exact-active.item__link-text:has-text('Обработка')"

    # Критерий 2: заголовок страницы Аналитика > Обработка
    ANALYTICS_PROCESSING_PAGE_HEADER = ".analytics-section__header:has-text('Обработка')"

    # Подпункт Инсайты в подменю Аналитика (до клика — is-inactive)
    ANALYTICS_SUBMENU_INSIGHTS = ".item__link-text.is-inactive:has-text('Инсайты')"

    # Критерий 1: подпункт Инсайты активен после клика
    ANALYTICS_INSIGHTS_ACTIVE = ".router-link-active.router-link-exact-active.item__link-text:has-text('Инсайты')"

    # Критерий 2: заголовок страницы Аналитика > Инсайты
    ANALYTICS_INSIGHTS_PAGE_HEADER = ".analytics-section__header:has-text('Инсайты')"

    # Подпункт Сравнение в подменю Аналитика (до клика — is-inactive)
    ANALYTICS_SUBMENU_COMPARISON = ".item__link-text.is-inactive:has-text('Сравнение')"

    # Критерий 1: подпункт Сравнение активен после клика
    ANALYTICS_COMPARISON_ACTIVE = ".router-link-active.router-link-exact-active.item__link-text:has-text('Сравнение')"

    # Критерий 2: заголовок страницы Аналитика > Сравнение
    ANALYTICS_COMPARISON_PAGE_HEADER = ".analytics-section__header:has-text('Сравнение')"

    # Пункт меню Настройки
    MENU_ITEM_SETTINGS = ".item__link-text:has-text('Настройки')"

    # Критерий: заголовок страницы Настройки
    SETTINGS_PAGE_TITLE = ".header__title:has-text('Настройки')"
