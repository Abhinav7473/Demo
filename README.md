# AI Workflow Habits Demo

FastAPI + Alembic + Postgres backend, TypeScript/Vite frontend, behind an nginx proxy, run with Docker Compose watch.

```bash
docker compose up --build --watch
```

Open http://localhost:8080. API is under http://localhost:8080/api (docs at `/api/docs`).

See [CLAUDE.md](CLAUDE.md) for project conventions.
