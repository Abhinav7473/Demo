from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Habit

app = FastAPI(title="AI Workflow Habits Demo", root_path="/api")


class HabitIn(BaseModel):
    name: str


class HabitOut(HabitIn):
    id: int


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/habits", response_model=list[HabitOut])
def list_habits(db: Session = Depends(get_db)):
    return db.scalars(select(Habit).order_by(Habit.id)).all()


@app.post("/habits", response_model=HabitOut, status_code=201)
def create_habit(body: HabitIn, db: Session = Depends(get_db)):
    habit = Habit(name=body.name)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit
