from sqlalchemy import Column, String, Float, DateTime, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timezone
from src.db.database import Base

class Field(Base):
    __tablename__ = "fields"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    crop_type = Column(String(100), nullable=True, index=True)
    area_hectares = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    soil_type = Column(String(100), nullable=True)
    irrigation_type = Column(String(50), nullable=True)
    planting_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
