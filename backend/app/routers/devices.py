from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/", response_model=schemas.RobotDeviceOut)
def create_device(device: schemas.RobotDeviceCreate, db: Session = Depends(database.get_db)):
    new_device = models.RobotDevice(**device.dict())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

@router.get("/", response_model=list[schemas.RobotDeviceOut])
def list_devices(db: Session = Depends(database.get_db)):
    return db.query(models.RobotDevice).order_by(models.RobotDevice.created_at.desc()).all()
