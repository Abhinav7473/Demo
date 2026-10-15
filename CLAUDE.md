# AI Workflow Habits Demo

Demo project showing good AI-assisted dev habits: memory files, skills, small verified steps.

## Stack
- **backend/** — Python 3.13, FastAPI, SQLAlchemy 2, Alembic, Postgres 17
- **frontend/** — TypeScript + Vite (vanilla, no framework)
- **Dockerfile** (root) — one multi-stage image: Node stage builds `frontend/` → copied into the Python stage at `/app/static`, served by FastAPI
- **nginx/** — reverse proxy on http://localhost:8089 → `app:8000`
- **compose.yaml** — `db`, `app`, `nginx`, with `develop.watch`: backend edits live-sync (uvicorn `--reload`); frontend edits rebuild the image

## Commands
- Run with live reload: `docker compose up --build --watch`
- Smoke test: `curl localhost:8089/api/health`
- New migration: `docker compose exec backend alembic revision --autogenerate -m "msg"`
- Apply migrations: `docker compose exec backend alembic upgrade head` (also runs on backend start)
- Frontend typecheck: `cd frontend && npx tsc`

## Conventions
- API routes live on the `api` router (prefix `/api`) in `app/main.py`; the static frontend is mounted at `/` last, so `/api` always wins.
- Every schema change goes through an Alembic migration in `backend/alembic/versions/` — never `Base.metadata.create_all`.
- Register new models by importing them in `app/models.py` (Alembic `env.py` imports that module).
- Frontend calls the API via relative `/api/...` paths only (see `frontend/src/api.ts`).
- Under watch: any change in `frontend/` or `backend/requirements.txt` rebuilds the app image; other `backend/` changes just sync.

## Memory
- `CLAUDE.md` (this file) — project-wide facts, checked in.
- `CLAUDE.local.md` — personal notes, gitignored.
- `.claude/skills/` — project skills (includes `find-skills` for discovering more).
