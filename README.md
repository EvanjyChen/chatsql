# ChatSQL

Interactive SQL learning platform with AI tutor assistance.

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- (Optional) MySQL for production databases

### 1. Clone and Setup
```bash
git clone https://github.com/jooguh-dev/chatsql.git
cd chatsql
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment (uses SQLite by default)
cp .env.example .env

# Initialize database with demo data
python manage.py setup_demo

# Start backend
python manage.py runserver 8000
```

### 3. Frontend Setup
```bash
# In a new terminal
cd chatsql-frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

### 4. Access Application

- Frontend: http://localhost:3001
- Backend API: http://localhost:8000
- Admin panel: http://localhost:8000/admin (credentials in `docs/superuser.txt`)

## Features

- Interactive SQL code editor with Monaco
- Real-time query execution and validation
- AI-powered tutor for SQL help (mock mode by default)
- Multiple practice databases (HR, eCommerce, School)
- Progress tracking and submissions

## Configuration

### Database Modes

**Local Development (default):** Uses SQLite, no additional setup required.

**Production MySQL:** Set these in `.env`:
```bash
DB_NAME=your_database
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=your_host
```

### AI Mode

**Mock (default):** Returns static responses, no API costs.

**Real OpenAI:** Set in `.env`:
```bash
OPENAI_MODE=real
OPENAI_API_KEY=your_key_here
```

## Development

- Backend: Django + Django REST Framework
- Frontend: React + TypeScript + Vite + Tailwind CSS
- Database: SQLite (dev) / MySQL (prod)

## Troubleshooting

**CSS not loading:** 
```bash
cd chatsql-frontend
rm -rf node_modules .vite
npm install
npm run dev
```

**CORS errors:** Check `CORS_ALLOWED_ORIGINS` in `settings.py` matches frontend port.

**Port conflicts:** Frontend defaults to 3001, backend to 8000. Change in `vite.config.ts` and restart.