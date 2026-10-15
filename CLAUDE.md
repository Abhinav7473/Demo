# AI Workflow Habits Demo

Demo project showing good AI-assisted dev habits: memory files, skills, small verified steps.

## Stack
- **backend/** — Python 3.13, FastAPI, SQLAlchemy 2, Alembic, Postgres 17
- **frontend/** — TypeScript + Vite (vanilla, no framework)
- **nginx/** — reverse proxy on http://localhost:8080 (`/api/*` → backend:8000, `/` → frontend:5173 with HMR websocket)
- **compose.yaml** — all services, with `develop.watch` for live sync

## Commands
- Run with live reload: `docker compose up --build --watch`
- Smoke test: `curl localhost:8080/api/health`
- New migration: `docker compose exec backend alembic revision --autogenerate -m "msg"`
- Apply migrations: `docker compose exec backend alembic upgrade head` (also runs on backend start)
- Frontend typecheck: `cd frontend && npx tsc`

## Conventions
- FastAPI uses `root_path="/api"`; nginx strips the `/api` prefix. Define routes without `/api`.
- Every schema change goes through an Alembic migration in `backend/alembic/versions/` — never `Base.metadata.create_all`.
- Register new models by importing them in `app/models.py` (Alembic `env.py` imports that module).
- Frontend calls the API via relative `/api/...` paths only (see `frontend/src/api.ts`).
- Changing `requirements.txt` or `package.json` triggers a container rebuild under watch.

## Memory
- `CLAUDE.md` (this file) — project-wide facts, checked in.
- `CLAUDE.local.md` — personal notes, gitignored.
- `.claude/skills/` — project skills (includes `find-skills` for discovering more).
