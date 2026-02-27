class UserManagementLocators:
    # Поля формы создания пользователя
    NAME_INPUT = "input[placeholder='Введите имя']"
    EMAIL_INPUT = "input[placeholder='Введите Email']"
    PHONE_INPUT = ".vti__input"
    PASSWORD_INPUT = "input[placeholder='Введите пароль']"

    # Выпадающий список роли
    ROLE_DROPDOWN_TOGGLE = ".v-select .vs__dropdown-toggle"
    ROLE_OPTION = ".vs__dropdown-option"

    # Страница edit-user: выпадающий список языка
    LANGUAGE_DROPDOWN_TOGGLE = ".users-grid__language .vs__dropdown-toggle"
    LANGUAGE_OPTION = ".users-grid__language .vs__dropdown-option"

    # Кнопка "Сохранить" на странице edit-user
    SAVE_EDIT_BTN = "button.button-main"