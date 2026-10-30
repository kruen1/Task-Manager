from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas
from .database import engine, get_db, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Task Manager API", version="1.0.0")


@app.get("/")
def root():
    return {"status": "ok", "message": "Task Manager API is running"}


# Создать задачу
@app.post("/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# Список задач
@app.get("/tasks", response_model=list[schemas.TaskOut])
def list_tasks(
    completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Task)
    if completed is not None:
        q = q.filter(models.Task.completed == completed)
    if priority:
        q = q.filter(models.Task.priority == priority)
    return q.order_by(models.Task.created_at.desc()).all()


# Статистика (должен идти ПЕРЕД /tasks/{task_id})
@app.get("/tasks/stats/summary", response_model=schemas.StatsOut)
def stats(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    by_priority = {"low": 0, "medium": 0, "high": 0}
    for t in tasks:
        by_priority[t.priority] = by_priority.get(t.priority, 0) + 1
    completed = sum(1 for t in tasks if t.completed)
    return {
        "total": len(tasks),
        "completed": completed,
        "pending": len(tasks) - completed,
        "by_priority": by_priority,
    }


# Получить по ID
@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task


# Обновить
@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task


# Удалить
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    db.delete(task)
    db.commit()
    return None


# Отметить выполненной
@app.patch("/tasks/{task_id}/complete", response_model=schemas.TaskOut)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    task.completed = True
    db.commit()
    db.refresh(task)
    return task
