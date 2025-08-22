from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/tasks", tags=["Logs"])

@router.get("/{device_id}/logs/", response_model=list[schemas.TaskExecutionLogOut])
def get_logs(device_id: str, db: Session = Depends(database.get_db)):
    return db.query(models.TaskExecutionLog).join(models.TaskSchedule).filter(models.TaskSchedule.device_id == device_id).all()
