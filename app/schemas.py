from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    priority: Literal["low", "medium", "high"] = "medium"


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    completed: Optional[bool] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class StatsOut(BaseModel):
    total: int
    completed: int
    pending: int
    by_priority: dict
