# Сервис бронирования переговорных комнат

Веб-сервис для автоматизации бронирования переговорных комнат в коворкинге.
Сотрудники могут просматривать доступность комнат и управлять своими бронированиями.
Администраторы имеют расширенные права — могут отменять любые бронирования.

## Стек технологий

- **Python 3.11+**
- **FastAPI** — веб-фреймворк
- **SQLAlchemy (async)** — ORM
- **PostgreSQL** — база данных
- **Alembic** — миграции
- **JWT** — аутентификация
- **Docker / docker-compose** — контейнеризация
- **Poetry** — управление зависимостями
- **pytest** — тестирование

---

## Запуск

### Вариант 1 — docker-compose (рекомендуется)


```bash
git clone https://github.com/ov4rlxrd/booking_app_test
cd booking_app_test

docker-compose up --build -d
```

Применить миграции и запустить скрипт seed.py ОБЯЗАТЕЛЬНО!!:

```bash
docker-compose exec app alembic upgrade head
docker-compose exec app python -m app.seed
```
После выполнения `python -m app.seed` (или `docker-compose exec app python -m app.seed`) 
в системе автоматически создаются два тестовых пользователя:

| Роль | Логин | Пароль |
|------|-------|--------|
| Администратор | `admin` | `admin123` |
| Сотрудник | `employee` | `emp123` |

**Перед началом работы необходимо получить JWT токен** через:

```bash
curl -X POST http://localhost:8001/users/token \
  -F "username=admin" \
  -F "password=admin123"
```

Приложение будет доступно по адресу: **http://localhost:8001**

Документация API (Swagger): **http://localhost:8001/docs**

---

### Вариант 2 — Docker

Убедитесь что PostgreSQL запущен и доступен. Создайте файл `.env`:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@host.docker.internal:5435/booking_db
SECRET_KEY=your-secret-key (в файле docker-compose лежит ключ)
```

Соберите и запустите образ:

```bash
docker build -t booking-app .
docker run -p 8001:8001 --env-file .env booking-app
```

---

### Вариант 3 — локально через Poetry

Установите зависимости:

```bash
poetry install
```

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5435/booking_db
SECRET_KEY=your-secret-key (в файле docker-compose лежит ключ)
```

Примените миграции:

```bash
poetry run alembic upgrade head
```

Запустите скрипт:

```bash
poetry run python -m app.seed
```

Запустите сервер:

```bash
poetry run uvicorn main:app --reload --port 8001
```

---

## Переменные окружения

| Переменная | Описание | Пример |
|---|---|---|
| `DATABASE_URL` | URL подключения к PostgreSQL | `postgresql+psycopg://postgres:postgres@localhost:5435/booking_db` |
| `SECRET_KEY` | Секретный ключ для подписи JWT | `my-secret-key` |

---

## Запуск тестов

```bash
poetry run pytest -v
```

Для тестов используется отдельная БД `test_booking_db`

```bash
docker exec -it booking_db psql -U postgres -c "CREATE DATABASE test_booking_db;"
```

---

## API

### Аутентификация

| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| `POST` | `/users` | Регистрация пользователя | Публичный |
| `POST` | `/users/token` | Получение JWT токена | Публичный |
| `GET` | `/users/me` | Информация о текущем пользователе | Авторизованный |

### Комнаты

| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| `GET` | `/rooms` | Список всех комнат | Авторизованный |
| `GET` | `/rooms/{room_id}` | Информация о комнате | Авторизованный |
| `GET` | `/rooms/available?booking_date=YYYY-MM-DD` | Доступность всех комнат на дату | Авторизованный |
| `GET` | `/rooms/available/{room_id}?booking_date=YYYY-MM-DD` | Доступность конкретной комнаты на дату | Авторизованный |

### Бронирования

| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| `POST` | `/booking` | Создать бронирование | Авторизованный |
| `GET` | `/booking/my` | Мои бронирования | Авторизованный |
| `DELETE` | `/booking/{booking_id}` | Отменить своё бронирование | Авторизованный |

### Администратор

| Метод | Путь | Описание | Доступ |
|---|---|---|---|
| `GET` | `/admin/bookings` | Все бронирования (с фильтром по дате) | Администратор |
| `DELETE` | `/admin/booking/{booking_id}` | Отменить любое бронирование | Администратор |

---

## Примеры работы

### Регистрация

```bash
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"login": "ivan", "password": "secret123",}'
```

```json
{
  "login": "ivan",
  "role": "employee"
}
```

### Получение токена

```bash
curl -X POST http://localhost:8001/users/token \
  -F "login=ivan" \
  -F "password=secret123"
```

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Доступность комнат на дату

```bash
curl http://localhost:8001/rooms/available?booking_date=2026-06-20 \
  -H "Authorization: Bearer eyJ..."
```

```json
[
  {
    "room_id": 1,
    "room_name": "Переговорная А",
    "date": "2026-06-20",
    "slots": [
      {
        "slot_id": 1,
        "start_time": "09:00:00",
        "end_time": "11:00:00",
        "is_available": true
      },
      {
        "slot_id": 2,
        "start_time": "11:00:00",
        "end_time": "13:00:00",
        "is_available": false
      }
    ]
  }
]
```

### Создание бронирования

```bash
curl -X POST http://localhost:8001/booking \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"room_slot_id": 1, "date": "2026-06-20"}'
```

```json
{
  "id": 1,
  "room_slot_id": 1,
  "date": "2026-06-20",
  "status": "active",
  "room_name": "Переговорная А",
  "start_time": "09:00:00",
  "end_time": "11:00:00"
}
```

### Отмена своего бронирования

```bash
curl -X DELETE http://localhost:8001/booking/1 \
  -H "Authorization: Bearer eyJ..."
```

Ответ: `204 No Content`

### Отмена любого бронирования (только админ)

```bash
curl -X DELETE http://localhost:8001/admin/booking/1 \
  -H "Authorization: Bearer eyJ..."
```

Ответ: `204 No Content`

---
