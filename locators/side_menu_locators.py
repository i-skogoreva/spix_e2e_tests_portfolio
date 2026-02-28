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
    # Субадмин: class="burger light" → совпадает с .burger
    # Менеджер:  class="burger"       → совпадает с .burger
    SIDEBAR_BURGER = ".burger"

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
    # Субадмин: class="item__link-text is-inactive" (внутри .sub-menu__items) → совпадает
    # Менеджер:  class="item__link-text"             (внутри .sub-menu__items) → совпадает
    ANALYTICS_SUBMENU_REVIEWS = ".sub-menu__items .item__link-text:has-text('Отзывы')"

    # Критерий 1: подпункт Отзывы активен после клика
    ANALYTICS_REVIEWS_ACTIVE = ".router-link-active.router-link-exact-active.item__link-text:has-text('Отзывы')"

    # Критерий 2: заголовок страницы Аналитика > Отзывы
    ANALYTICS_REVIEWS_PAGE_HEADER = ".analytics-section__header:has-text('Отзывы')"

    # Подпункт Обработка в подменю Аналитика
    ANALYTICS_SUBMENU_PROCESSING = ".sub-menu__items .item__link-text:has-text('Обработка')"

    # Критерий 1: подпункт Обработка активен после клика
    ANALYTICS_PROCESSING_ACTIVE = ".router-link-active.router-link-exact-active.item__link-text:has-text('Обработка')"

    # Критерий 2: заголовок страницы Аналитика > Обработка
    ANALYTICS_PROCESSING_PAGE_HEADER = ".analytics-section__header:has-text('Обработка')"

    # Подпункт Инсайты в подменю Аналитика
    ANALYTICS_SUBMENU_INSIGHTS = ".sub-menu__items .item__link-text:has-text('Инсайты')"

    # Критерий 1: подпункт Инсайты активен после клика
    ANALYTICS_INSIGHTS_ACTIVE = ".router-link-active.router-link-exact-active.item__link-text:has-text('Инсайты')"

    # Критерий 2: заголовок страницы Аналитика > Инсайты
    ANALYTICS_INSIGHTS_PAGE_HEADER = ".analytics-section__header:has-text('Инсайты')"

    # Подпункт Сравнение в подменю Аналитика
    ANALYTICS_SUBMENU_COMPARISON = ".sub-menu__items .item__link-text:has-text('Сравнение')"

    # Критерий 1: подпункт Сравнение активен после клика
    ANALYTICS_COMPARISON_ACTIVE = ".router-link-active.router-link-exact-active.item__link-text:has-text('Сравнение')"

    # Критерий 2: заголовок страницы Аналитика > Сравнение
    ANALYTICS_COMPARISON_PAGE_HEADER = ".analytics-section__header:has-text('Сравнение')"

    # Пункт меню Настройки
    MENU_ITEM_SETTINGS = ".item__link-text:has-text('Настройки')"

    # Критерий: заголовок страницы Настройки
    SETTINGS_PAGE_TITLE = ".header__title:has-text('Настройки')"

    # Ховер-меню "Нужна помощь?"
    HELP_MENU_TRIGGER = ".item__link:has(.item__link-text:has-text('Нужна помощь?'))"
    HELP_INSTRUCTIONS_BTN = ".hover-link:has-text('Смотреть инструкции')"
    HELP_SUPPORT_BTN = ".hover-link:has-text('Написать в поддержку')"

    # Ховер-меню профиля
    PROFILE_MENU_TRIGGER = ".sidebar__footer-link-wrapper[aria-haspopup='menu']"
    PROFILE_MY_PROFILE_BTN = ".hover-link:has-text('Мой профиль')"
    PROFILE_COMPANY_BTN = ".hover-link:has-text('Компания')"
    PROFILE_HISTORY_BTN = ".hover-link:has-text('История обработки')"
    PROFILE_LOGOUT_BTN = ".hover-link:has-text('Выйти')"

    # Модальное окно подтверждения выхода
    LOGOUT_CONFIRM_YES_BTN = "button.profile__save:not(.ghost)"

    # ── Узкое меню (narrow) ───────────────────────────────────────────────

    # Попап-триггеры (клик или ховер открывают .tooltip-menu)
    MENU_ITEM_REVIEWS_NARROW = ".sub-menu__header:has(.item__link-text:has-text('Отзывы'))"
    MENU_ITEM_ANALYTICS_NARROW = ".sub-menu__header:has(.item__link-text:has-text('Аналитика'))"

    # Попап узкого меню (Отзывы и Аналитика)
    NARROW_POPUP = ".tooltip-menu"

    # Простые иконки (кликабельны напрямую по aria-label)
    MENU_ITEM_CHATS_NARROW = "a.item__link[aria-label='Чаты']"
    MENU_ITEM_PRODUCTS_NARROW = "a.item__link[aria-label='Товары']"
    MENU_ITEM_PLACES_NARROW = "a.item__link[aria-label='Места']"
    MENU_ITEM_CLIENTS_NARROW = "a.item__link[aria-label='Клиенты']"
    MENU_ITEM_SETTINGS_NARROW = "a.item__link[aria-label='Настройки']"

    # Подпункт Обработка внутри tooltip-попапа узкого меню
    # В узком режиме попап рендерится в .tooltip-menu, а не в .sub-menu__items
    ANALYTICS_SUBMENU_PROCESSING_NARROW = ".tooltip-menu .item__link-text:has-text('Обработка')"
