import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base

class RobotDevice(Base):
    __tablename__ = "robot_devices"
    device_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class TaskDefinition(Base):
    __tablename__ = "task_definitions"
    task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_name = Column(String, nullable=False)
    parameters_schema = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class TaskSchedule(Base):
    __tablename__ = "task_schedules"
    schedule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("robot_devices.device_id"), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("task_definitions.task_id"), nullable=False)
    scheduled_time = Column(TIMESTAMP(timezone=True), nullable=False)
    parameters = Column(JSON, nullable=False)
    status = Column(String, default="queued")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class TaskExecutionLog(Base):
    __tablename__ = "task_execution_logs"
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("task_schedules.schedule_id"), nullable=False)
    executed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    result = Column(String, nullable=False)
    success = Column(Boolean, default=True)
