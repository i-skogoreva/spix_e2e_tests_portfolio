class OperatorLocators:
    """Локаторы для роли Оператор.

    Оператор НЕ имеет бокового меню. Навигация осуществляется через шапку страницы.
    """

    # ── Шапка: ссылка «Чаты» ─────────────────────────────────────────────
    HEADER_CHATS_LINK = ".header-chats-link"

    # ── Шапка: иконка профиля — кружок с инициалами (без внутренних ссылок)
    HEADER_PROFILE_TRIGGER = ".initials__content"

    # ── Выпадающее меню профиля (класс .statistic__tools-btn / .statistic__name)
    PROFILE_MY_PROFILE_BTN   = ".statistic__tools-btn:has-text('Мой профиль')"
    PROFILE_INSTRUCTIONS_BTN = ".statistic__tools-btn:has-text('Смотреть инструкции')"
    PROFILE_SUPPORT_BTN      = ".statistic__tools-btn:has-text('Написать в поддержку')"
    PROFILE_HISTORY_BTN      = "button.statistic__name:has-text('История обработки')"
    PROFILE_LOGOUT_BTN       = ".statistic__tools-btn:has-text('Выйти')"

    # ── Подтверждение выхода ──────────────────────────────────────────────
    LOGOUT_CONFIRM_YES_BTN = "button.btns__confirm"

    # ── Шапка: dropdown переключения источника (Маркетплейсы / Карты) ────
    HEADER_SOURCE_BTN   = "button.custom-v-menu-options__btn"
    SOURCE_OPTION_KARTY = "button.custom-v-menu-options__option:has-text('Карты')"
