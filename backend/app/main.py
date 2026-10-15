from pathlib import Path

from fastapi import APIRouter, Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Habit, Principle

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI(title="AI Workflow Habits Demo", docs_url="/api/docs", openapi_url="/api/openapi.json")
api = APIRouter(prefix="/api")


class HabitIn(BaseModel):
    name: str


class HabitOut(HabitIn):
    id: int


class PrincipleOut(BaseModel):
    id: int
    code: str
    source: str
    category: str
    title: str
    summary: str
    example: str


@api.get("/health")
def health():
    return {"status": "ok"}


@api.get("/habits", response_model=list[HabitOut])
def list_habits(db: Session = Depends(get_db)):
    return db.scalars(select(Habit).order_by(Habit.id)).all()


@api.post("/habits", response_model=HabitOut, status_code=201)
def create_habit(body: HabitIn, db: Session = Depends(get_db)):
    habit = Habit(name=body.name)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@api.get("/principles", response_model=list[PrincipleOut])
def list_principles(source: str | None = None, q: str | None = None, db: Session = Depends(get_db)):
    stmt = select(Principle).order_by(Principle.id)
    if source:
        stmt = stmt.where(Principle.source == source)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(Principle.title.ilike(like) | Principle.summary.ilike(like) | Principle.example.ilike(like))
    return db.scalars(stmt).all()


app.include_router(api)

# Built frontend (copied in from the Node build stage). Mounted last so /api wins.
if STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="frontend")
