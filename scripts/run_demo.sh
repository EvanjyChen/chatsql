#!/usr/bin/env bash
# Run ChatSQL demo setup (backend + frontend)
# Usage:
#   ./scripts/run_demo.sh         # full setup and start both servers
#   ./scripts/run_demo.sh --no-start   # setup only, do not start servers
#   ./scripts/run_demo.sh --no-front   # skip frontend install/start
#   ./scripts/run_demo.sh --no-back    # skip backend steps

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

# Flags
START_SERVERS=true
DO_FRONT=true
DO_BACK=true

for arg in "$@"; do
  case "$arg" in
    --no-start) START_SERVERS=false ;;
    --no-front) DO_FRONT=false ;;
    --no-back) DO_BACK=false ;;
    -h|--help)
      sed -n '1,160p' "$0"
      exit 0 ;;
    *) echo "Unknown arg: $arg"; exit 1 ;;
  esac
done

echo "[run_demo] Root: $ROOT_DIR"

if [ "$DO_BACK" = true ]; then
  echo "[run_demo] Setting up backend..."
  # Python venv
  if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "[run_demo] Created venv"
  else
    echo "[run_demo] venv already exists"
  fi

  # Install Python deps
  echo "[run_demo] Installing Python dependencies (this may take a while)..."
  venv/bin/python -m pip install --upgrade pip setuptools wheel
  venv/bin/pip install -r requirements.txt

  # Ensure .env exists (do NOT overwrite if present)
  if [ ! -f .env ]; then
    if [ -f .env.example ]; then
      cp .env.example .env
      echo "[run_demo] Copied .env.example -> .env (edit .env to add secrets if needed)"
    else
      echo "[run_demo] No .env or .env.example found; continuing with defaults"
    fi
  else
    echo "[run_demo] .env exists (will not overwrite)"
  fi

  echo "[run_demo] Running Django migrations..."
  venv/bin/python manage.py makemigrations --noinput || true
  venv/bin/python manage.py migrate --noinput

  echo "[run_demo] Creating demo data (setup_demo)..."
  # setup_demo uses DEMO_SUPERUSER_* env vars if provided; otherwise defaults will be used
  export DEMO_SUPERUSER_USERNAME=${DEMO_SUPERUSER_USERNAME:-demo_admin}
  export DEMO_SUPERUSER_EMAIL=${DEMO_SUPERUSER_EMAIL:-demo_admin@example.com}
  export DEMO_SUPERUSER_PASSWORD=${DEMO_SUPERUSER_PASSWORD:-DemoPass123!}
  venv/bin/python manage.py setup_demo || true

  echo "[run_demo] Loading all Workshop exercises (WS1-WS11)..."
  venv/bin/python manage.py load_all_exercises || true

  echo "[run_demo] Applying seed SQL into default DB (apply_seed)..."
  venv/bin/python manage.py apply_seed || true
fi

if [ "$DO_FRONT" = true ]; then
  echo "[run_demo] Setting up frontend (Vite + React)..."
  FRONT_DIR="$ROOT_DIR/chatsql-frontend"
  if [ -d "$FRONT_DIR" ]; then
    cd "$FRONT_DIR"
    if [ ! -f package.json ]; then
      echo "[run_demo] frontend package.json not found in $FRONT_DIR"; exit 1
    fi
    echo "[run_demo] Installing frontend npm packages (this may take a while)..."
    # Prefer npm; if not present, bail with message
    if ! command -v npm >/dev/null 2>&1; then
      echo "npm not found - please install Node.js and npm to run frontend setup"; exit 1
    fi
    npm install
    # create frontend .env for API base if not exists
    if [ ! -f .env ]; then
      echo "VITE_API_BASE_URL=http://localhost:8000/api" > .env
      echo "[run_demo] Created chatsql-frontend/.env with VITE_API_BASE_URL"
    fi
    cd "$ROOT_DIR"
  else
    echo "[run_demo] Frontend directory not found at $FRONT_DIR - skipping frontend setup"
  fi
fi

PIDS=()

if [ "$START_SERVERS" = true ]; then
  if [ "$DO_BACK" = true ]; then
    echo "[run_demo] Starting Django dev server (127.0.0.1:8000)..."
    venv/bin/python manage.py runserver 127.0.0.1:8000 &>/tmp/chatsql-server.log &
    PID=$!
    PIDS+=("$PID")
    echo "[run_demo] Django PID: $PID, logs: /tmp/chatsql-server.log"
    sleep 1
  fi

  if [ "$DO_FRONT" = true ]; then
    echo "[run_demo] Starting Vite dev server (http://localhost:3000)..."
    # run in frontend dir
    (cd "$ROOT_DIR/chatsql-frontend" && npm run dev &>/tmp/chatsql-frontend.log &)
    PID=$!
    PIDS+=("$PID")
    echo "[run_demo] Vite PID: $PID, logs: /tmp/chatsql-frontend.log"
    sleep 1
  fi

  echo "[run_demo] Servers started. Give them a few seconds to boot up."
  echo "  Backend: http://127.0.0.1:8000"
  echo "  Frontend: http://127.0.0.1:3000"
fi

echo "[run_demo] Done. Process PIDs: ${PIDS[*]:-none}"
echo "If you want to stop servers: pkill -f 'manage.py runserver' ; pkill -f 'vite' || true"
