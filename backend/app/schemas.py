from pydantic import BaseModel, Field
from typing import Optional, Dict, Literal
from datetime import datetime
import uuid

class RobotDeviceCreate(BaseModel):
    device_name: str
    model: str

class RobotDeviceOut(RobotDeviceCreate):
    device_id: uuid.UUID
    created_at: datetime
    class Config: orm_mode = True

class TaskDefinitionCreate(BaseModel):
    task_name: str
    parameters_schema: Dict

class TaskDefinitionOut(TaskDefinitionCreate):
    task_id: uuid.UUID
    created_at: datetime
    class Config: orm_mode = True

class TaskScheduleCreate(BaseModel):
    task_id: uuid.UUID
    scheduled_time: datetime
    parameters: Dict

class TaskScheduleOut(TaskScheduleCreate):
    schedule_id: uuid.UUID
    device_id: uuid.UUID
    status: Literal["queued","running","completed","failed"]
    created_at: datetime
    class Config: orm_mode = True

class TaskExecutionLogCreate(BaseModel):
    result: str
    success: bool

class TaskExecutionLogOut(TaskExecutionLogCreate):
    log_id: uuid.UUID
    executed_at: datetime
    class Config: orm_mode = True
