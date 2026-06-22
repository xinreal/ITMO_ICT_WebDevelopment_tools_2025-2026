# Hackathon API

FastAPI laboratory project for hackathon management.

## Setup

```bash
python -m venv .venv
```

```bash
pip install -r requirements.txt
```

Create `.env` from `.env.example` and set real values for `DB_ADMIN` and `JWT_SECRET_KEY`.

```bash
alembic upgrade head
```

```bash
uvicorn main:app --reload
```

Swagger UI is available at:

```text
http://127.0.0.1:8000/docs
```
