# Wallet API

REST API для управления кошельками пользователей. Реализован на FastAPI с PostgreSQL, поддерживает конкурентные операции через пессимистичную блокировку (`SELECT FOR UPDATE`).

## Технологический стек

- **FastAPI** — асинхронный веб-фреймворк
- **PostgreSQL 16** — база данных
- **SQLAlchemy 2.0** — асинхронный ORM (`asyncpg`)
- **Alembic** — миграции БД
- **Docker / Docker Compose** — контейнеризация
- **pytest + httpx** — тестирование

---

## Быстрый старт

```bash
pip3 install -r requirements.txt
```

```bash
docker compose build --no-cache
```

```bash
docker compose up
```

---

## Запуск тестов

```bash
docker run --rm \
  -e PYTHONPATH=/app \
  -e DATABASE_URL=postgresql+asyncpg://wallet:wallet@db:5432/wallet_test \
  -e DATABASE_URL_SYNC=postgresql://wallet:wallet@db:5432/wallet_test \
  --network task_default \
  task-api \
  python -m pytest /app/tests/ -v
```

---

## API Endpoints

### Изменение баланса кошелька

```
POST /api/v1/wallets/{wallet_uuid}/operation
```

**Тело запроса:**
```json
{
  "operation_type": "DEPOSIT",
  "amount": 1000
}
```

`operation_type`: `DEPOSIT` (пополнение) или `WITHDRAW` (снятие)

**Ответ:**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "balance": "1000.00"
}
```

---

### Получение баланса кошелька

```
GET /api/v1/wallets/{wallet_uuid}
```

**Ответ:**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "balance": "1000.00"
}
```