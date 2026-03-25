class FinanceManagementLocators:
    # Страница биллинга /settings-company/billing
    UPGRADE_BTN = ".billing-package__btn"
    CURRENT_PLAN_TITLE = ".billing-package__col-title"

    # Страница выбора тарифа /billing-plan
    FREE_PLANS_SECTION = "h2.billing-plan__title:has-text('Бесплатные тарифы')"
    PRO_PLAN_CONNECT_BTN = ".card:has(.card__name:has-text('ПРО')) .card__button"
    BUSINESS_PLAN_CONNECT_BTN = ".card:has(.card__name:has-text('БИЗНЕС')) .card__button"
    CONFIRM_BTN = "button:has-text('Уверен')"
    SUCCESS_BTN = "button:has-text('Отлично')"

    # Токены
    ADD_TOKENS_BTN = ".billing-balance__btn-add-tokens"
    TOKEN_AMOUNT_INPUT = ".ppopup-add-tokens__input"
    TOKEN_COMMENT_INPUT = ".popup-add-tokens__textarea"
    TOKEN_SAVE_BTN = ".popup-add-tokens__buttons button:has-text('Сохранить')"
    PACKAGE_BALANCE = ".billing-balance__consumption"

    # Счета (таблица на вкладке "Счета")
    INVOICES_TAB = ".base-tabs__btn:has-text('Счета')"
    INVOICE_ROW = ".table-row"
    INVOICE_STATUS = ".item-cell.status-warn"

    # Платёжная информация
    ADD_PAYMENT_BTN = ".payment-info__card-footer button"
    BANK_ACCOUNT_TAB = "text='Рас. счет'"
    ORG_NAME_INPUT = "input.name-company"
    FIRST_SUGGESTION = ".form-field__suggestion"
    SAVE_PAYMENT_BTN = "button:has-text('Сохранить')"
    PAYMENT_INFO_SECTION = ".payment-info"

    # Уведомления (Vue-Toastification)
    TOAST_BODY = ".Vue-Toastification__toast-body"
