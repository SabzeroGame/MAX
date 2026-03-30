# MAX Portfolio (Django)

Портфолио-проект для студенческого кружка или спортивной секции.

## Что уже реализовано

- Публичная витрина проектов с поиском и фильтрацией по категориям.
- Современный UI на Bootstrap + кастомный CSS + визуальные блоки (карточки, counters, skill-map).
- Переключение темы: светлая ↔ тёмная (с сохранением в localStorage).
- Поддержка русского и английского интерфейса через Django i18n (переключение языка в хедере).
- Раздел команды и контактная форма.
- Django Admin для управления проектами, участниками и входящими сообщениями.
- DRF API для опубликованных проектов.

## Стек выполнения

- Python 3.13
- Django
- SQLite (основная и единственная БД проекта)

## Быстрый локальный запуск

### 1. Перейти в проект

```bash
cd ~/Desktop/MAX/max_portfolio
```

### 2. Создать и активировать виртуальное окружение

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Подготовить `.env`

```bash
cp .env.example .env
```

Для локального показа через `python manage.py runserver` оставь в `.env`:

```env
DJANGO_ENV=dev
DJANGO_DEBUG=1
DJANGO_USE_SQLITE=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Выполнить миграции

```bash
python manage.py migrate
```

### 6. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 7. Запустить проект

```bash
python manage.py runserver
```

Проект откроется по адресу `http://127.0.0.1:8000/`.

Админка проекта откроется по адресу `http://127.0.0.1:8000/admin/`.

## Проверка проекта

```bash
python manage.py check
python manage.py test
```