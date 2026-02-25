class ClientFilterLocators:
    # Дропдаун выбора клиента в шапке
    CLIENT_DROPDOWN_TOGGLE = ".header-client-filter__clients .vs__dropdown-toggle"
    CLIENT_SEARCH_INPUT = ".header-client-filter__clients input.vs__search"
    CLIENT_SELECTED = ".header-client-filter__clients .vs__selected"
    CLIENT_OPTION_TEMPLATE = ".vs__dropdown-menu .vs__dropdown-option:has-text('{client_name}')"

    # Лоадер при смене клиента (перезагрузка страницы отзывов)
    PAGE_LOADER = ".loader-wrapper"
