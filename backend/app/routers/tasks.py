from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, utils
from datetime import datetime
from uuid import UUID

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/definitions/", response_model=schemas.TaskDefinitionOut)
def create_task_definition(task: schemas.TaskDefinitionCreate, db: Session = Depends(database.get_db)):
    new_task = models.TaskDefinition(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/definitions/", response_model=list[schemas.TaskDefinitionOut])
def list_task_definitions(db: Session = Depends(database.get_db)):
    return db.query(models.TaskDefinition).order_by(models.TaskDefinition.created_at.desc()).all()

@router.post("/{device_id}/schedule/", response_model=schemas.TaskScheduleOut)
def schedule_task(device_id: UUID, schedule: schemas.TaskScheduleCreate, db: Session = Depends(database.get_db)):
    device = db.query(models.RobotDevice).filter(models.RobotDevice.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    task_def = db.query(models.TaskDefinition).filter(models.TaskDefinition.task_id == schedule.task_id).first()
    if not task_def:
        raise HTTPException(status_code=404, detail="Task definition not found")

    ok, err = utils.validate_parameters(task_def.parameters_schema, schedule.parameters)
    if not ok:
        raise HTTPException(status_code=400, detail=f"Invalid parameters: {err}")

    if schedule.scheduled_time < datetime.utcnow():
        # Allow past time? Usually no—treat as immediate run request
        # For spec compliance, keep it, but warn via 400
        raise HTTPException(status_code=400, detail="scheduled_time must be in the future (UTC)")

    new_schedule = models.TaskSchedule(device_id=device_id, **schedule.dict())
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

@router.get("/{device_id}/scheduled/", response_model=list[schemas.TaskScheduleOut])
def get_scheduled_tasks(device_id: UUID, db: Session = Depends(database.get_db)):
    return (
        db.query(models.TaskSchedule)
          .filter(models.TaskSchedule.device_id == device_id)
          .order_by(models.TaskSchedule.scheduled_time.asc())
          .all()
    )

@router.post("/{schedule_id}/execute/", response_model=schemas.TaskExecutionLogOut)
def execute_task(schedule_id: UUID, log: schemas.TaskExecutionLogCreate, db: Session = Depends(database.get_db)):
    schedule = db.query(models.TaskSchedule).filter(models.TaskSchedule.schedule_id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Task schedule not found")

    schedule.status = "completed" if log.success else "failed"
    new_log = models.TaskExecutionLog(schedule_id=schedule_id, **log.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log
