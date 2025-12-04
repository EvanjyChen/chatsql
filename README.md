# ChatSQL Backend

Django REST API backend for ChatSQL - interactive SQL learning with AI tutor.

## Quickstart

1. Create and activate virtualenv

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill values

```bash
cp .env.example .env
# edit .env to add DB credentials and OPENAI_API_KEY
```

4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser

```bash
python manage.py createsuperuser
```

6. Run server

```bash
python manage.py runserver
```

7. API endpoints

- `GET /api/schemas/`
- `GET /api/exercises/`
- `GET /api/exercises/<id>/`
- `POST /api/exercises/<id>/execute/` (payload: `{"query": "SELECT ..."}`)
- `POST /api/exercises/<id>/submit/` (payload: `{"query": "SELECT ..."}`)

Notes: You need MySQL instances for main and practice DBs as defined in the `.env` file.
