# E2E-автотесты

Проект автоматизации E2E-тестирования веб-приложения на базе Python + Playwright + Pytest.
Проект демонстрирует построение поддерживаемого автотестового фреймворка с использованием Page Object Model, pytest fixtures, тестовых данных, кастомных assertions и Allure Reports.
Примечание: репозиторий подготовлен как portfolio-проект. Конфиденциальные данные, реальные URL, учётные записи и внутренние идентификаторы удалены или заменены на демонстрационные значения.

Tech Stack
Python 3.11
Playwright
Pytest
Allure Report
Faker
python-dotenv
Page Object Model (POM)
Dataclasses
CSS selectors
Git / GitHub

Возможности проекта
E2E-тестирование пользовательских сценариев
Авторизация пользователей с различными ролями
Работа с UI через Playwright
Использование Page Object Model
Общие pytest fixtures
Разделение тестовых данных и логики тестов
Генерация тестовых данных с помощью Faker
Кастомные assertions
Формирование Allure-отчётов
Организация тестов по функциональным областям

## 1. Установка PyCharm

1. Перейти на сайт [JetBrains PyCharm](https://www.jetbrains.com/pycharm/download/)
2. Скачать версию **Professional** или **Community** (Community бесплатная, её достаточно)
3. Запустить установщик:
   - **macOS**: открыть `.dmg`, перетащить PyCharm в папку Applications
   - **Windows**: запустить `.exe`, следовать шагам мастера установки, на шаге "Installation Options" отметить "Add to PATH"
4. Запустить PyCharm, при первом запуске выбрать тему и настройки по умолчанию

## 2. Установка Python

Проект использует **Python 3.11**.

### macOS

```bash
# Через Homebrew (рекомендуется)
brew install python@3.11
```

### Windows

1. Скачать установщик с [python.org](https://www.python.org/downloads/)
2. При установке **обязательно** отметить галочку **"Add Python to PATH"**
3. Нажать "Install Now"

### Проверка установки

```bash
python3 --version
# Python 3.11.x
```

## 3. Установка Git

### macOS

```bash
brew install git
```

### Windows

Скачать установщик с [git-scm.com](https://git-scm.com/downloads) и установить с настройками по умолчанию.

### Проверка

```bash
git --version
```

## 4. Клонирование репозитория и открытие в PyCharm

```bash
git clone <URL_репозитория>
```

Открыть проект в PyCharm: **File > Open** и выбрать папку `spix_playwright`.

## 5. Настройка виртуального окружения в PyCharm

1. Открыть **File > Settings** (macOS: **PyCharm > Settings**)
2. Перейти в **Project: spix_playwright > Python Interpreter**
3. Нажать шестерёнку справа > **Add Interpreter > Add Local Interpreter**
4. Выбрать **Virtualenv Environment > New**
5. В поле "Base interpreter" выбрать Python 3.11
6. Location оставить по умолчанию (`.venv` в корне проекта)
7. Нажать **OK**

Или через терминал:

```bash
python3.11 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

## 6. Установка зависимостей

В терминале PyCharm (убедиться, что виртуальное окружение активировано — в начале строки будет `(.venv)`):

```bash
pip install -r requirements.txt
```

## 7. Установка браузеров Playwright

```bash
playwright install chromium
```

## 8. Настройка переменных окружения

Создать файл `.env` в корне проекта (он не хранится в Git):

```
SUBADMIN_PHONE_NUMBER = +7 XXXXXXXXXX
SUBADMIN_PASSWORD = ваш_пароль
MANAGER_PHONE_NUMBER = +7 XXXXXXXXXX
MANAGER_PASSWORD = ваш_пароль
OPERATOR_PHONE_NUMBER = +7 XXXXXXXXXX
OPERATOR_PASSWORD = ваш_пароль
```

Запросить актуальные значения у команды.

## 9. Установка Allure (для отчётов)

### macOS

```bash
brew install allure
```

### Windows

```bash
scoop install allure
```

Или скачать вручную с [GitHub Allure](https://github.com/allure-framework/allure2/releases) и добавить `bin/` в PATH.

### Проверка

```bash
allure --version
```

## 10. Запуск тестов

```bash
# Все тесты
pytest

# Конкретный файл
pytest tests/test_user_authorization.py

# Конкретный тест по имени
pytest -k "test_tc_0001"

# С подробным выводом
pytest -v
```

Результаты Allure автоматически сохраняются в папку `allure-results/`.

## 11. Просмотр Allure-отчёта

```bash
allure serve allure-results
```

Откроется браузер с интерактивным отчётом.

## Структура проекта

```
spix_playwright/
  conftest.py            # pytest-фикстуры (page, get_cookies, authorized_user)
  pytest.ini             # конфигурация pytest + Allure
  requirements.txt       # зависимости Python
  .env                   # секреты (не в Git)
  tests/                 # тест-кейсы с декораторами Allure
  pages/                 # page-объекты (наследуются от BasePage)
    base_page.py         # базовые методы взаимодействия с Playwright
  locators/              # CSS-селекторы, сгруппированные по тест-сьютам
  data/
    endpoints.py         # URL-эндпоинты
    dataclasses/         # тестовые данные (dataclasses), по файлу на тест-сьют
  utils/
    assertions/          # кастомные ассерты
    generators/          # генераторы данных (Faker)
  docs/                  # документация тестов (test_*.md)
```

## Частые проблемы

| Проблема | Решение |
|----------|---------|
| `playwright install` падает | Проверить доступ к сети, попробовать с `--with-deps` |
| Тесты не находятся | Убедиться, что файлы начинаются с `test_`, классы с `Test`, функции с `test_` |
| `.env` не подхватывается | Проверить, что файл лежит в корне проекта и нет лишних пробелов |
| Браузер не открывается | Выполнить `playwright install chromium` |
| Allure не найден | Установить Allure и проверить, что он добавлен в PATH |