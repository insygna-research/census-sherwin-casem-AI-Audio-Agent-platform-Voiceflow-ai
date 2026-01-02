from sqlalchemy import Column, String, DateTime, Enum, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class CallDirection(enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class CallStatus(enum.Enum):
    INITIATED = "initiated"
    RINGING = "ringing"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Call(Base):
    __tablename__ = "calls"
    
    id = Column(String, primary_key=True)
    direction = Column(Enum(CallDirection))
    from_number = Column(String)
    to_number = Column(String)
    status = Column(Enum(CallStatus))
    duration = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
