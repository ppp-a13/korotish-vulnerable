# korotish - сокращатель ссылок

URL-сокращатель на **FastAPI** и **PostgreSQL**, в который
намеренно внедрены типовые веб-уязвимости (SQL injection, stored XSS, IDOR,
JWT misconfiguration, SSRF).

> **Приложение намеренно небезопасно.**

## Уязвимости

Каждая внедрённая уязвимость (расположение, PoC и фикс) описана в
[`security-review.md`](./security-review.md). Фиксы только «на бумаге» и
не применены в `main`.

| # | Уязвимость | OWASP категория |
|---|---|---|
| 1 | SQL Injection | A03:2021 – Injection |
| 2 | Stored XSS | A03:2021 – Injection |
| 3 | IDOR | A01:2021 – Broken Access Control |
| 4 | JWT misconfiguration | A02:2021 – Cryptographic Failures |
| 5 | SSRF | A10:2021 – Server-Side Request Forgery |

## Стек

FastAPI · SQLAlchemy (async) · PostgreSQL · PyJWT · Jinja2 · Docker

## Функциональность

- Регистрация/логин с JWT в HTTP-only cookie
- Создание коротких ссылок (анонимно или под аккаунтом), с опциональным кастомным alias
- Учёт переходов по ссылке
- Личный дашборд и поиск по своим ссылкам
- Панель администратора (пользователи, ссылки, суммарные переходы)

## Запуск

```bash
git clone https://github.com/ppp-a13/korotish-vulnerable.git
cd korotish-vulnerable

# поднять БД
docker compose up -d db

# поднять backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

alembic upgrade head
uvicorn app.main:app --reload
```

Приложение доступно на `http://localhost:8000`.

## Структура проекта

```
backend/
- app/
-- routes/         # HTML + API routes
-- services/       # бизнес-логика
-- repositories/   # доступ к БД
-- models/         # SQLAlchemy модели
-- schemas/        # pydantic схемы
- templates/       # Jinja2 шаблоны
```
