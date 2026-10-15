# AI Workflow Habits Demo

FastAPI + Alembic + Postgres backend and a TypeScript/Vite frontend, built into one multi-stage image, behind an nginx proxy, run with Docker Compose watch.

```bash
docker compose up --build --watch
```

Open http://localhost:8089. API is under http://localhost:8089/api (docs at `/api/docs`).

See [CLAUDE.md](CLAUDE.md) for project conventions.
