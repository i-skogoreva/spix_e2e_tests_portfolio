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
