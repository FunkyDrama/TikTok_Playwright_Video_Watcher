# TikTok Playwright Video Watcher 🤖

Автоматизований бот для перегляду відео на [TikTok](https://www.tiktok.com) із використанням Python і Playwright.

---

## 🚀 Особливості

* Авторизація через email/пароль
* Пошук відео за ключовим запитом
* Імовірнісне пропускання відео (`skip_percent`)
* Відтворення відео або скіп залежно від налаштувань
* Виведення в консоль:

  * Ідентифікатор або посилання на відео
  * Статус: переглянуто чи пропущено

---

## 📋 Prerequisites

* **Python 3.12+**
* **[Poetry](https://python-poetry.org/)** для керування залежностями
* **Google Chrome** (для підтримки пропрієтарних кодеків)
* `.env` файл з параметрами середовища

---

## 🛠️ Встановлення

1. Клонуйте репозиторій:

   ```bash
   git clone https://github.com/FunkyDrama/TikTok_Playwright_Video_Watcher.git
   cd TikTok_Playwright_Video_Watcher
   ```

2. Встановіть залежності через Poetry:

   ```bash
   poetry install
   ```

3. Ініціалізуйте середовище:

   ```bash
   poetry shell
   ```

---

## ⚙️ Налаштування

Створіть файл `.env` у корені проєкту (або в директорії `../.env`) і додайте:

```dotenv
TIKTOK_EMAIL=your_email@example.com
TIKTOK_PASS=your_password
SKIP_PERCENT=12      # Відсоток відео, які будуть пропущені
MAX_VIDEOS=10        # Максимальна кількість відео для перегляду
SEARCH_QUERY=cats    # Запит для пошуку відео
```

> Замість `your_email@example.com` та `your_password` вкажіть свої дані для входу до TikTok.

---

## 🎬 Використання

Запустіть скрипт через Poetry:

```bash
poetry run python main.py
```

За замовчуванням бот запускається з головним вікном браузера (не headless). Щоб увімкнути headless-режим, змініть виклик у `main.py`:

```python
TikTokViewer().run(headless=True)
```

---

## 🗂️ Структура проєкту

```
TikTok_Playwright_Video_Watcher/
├── main.py           # Точка входу
├── viewer.py         # Логіка TikTokViewer
├── settings.py       # Зчитування налаштувань через pydantic-settings
├── .env              # Файл .env (додайте свій за прикладом вище)
├── pyproject.toml    # Опис проєкту та залежностей Poetry
├── poetry.lock       # Зафіксовані версії встановлених залежностей
└── README.md         # Документація (цей файл)
```

---

## Анотація

Цей проєкт був створений як тестове завдання! Він не є комерційним!
---
