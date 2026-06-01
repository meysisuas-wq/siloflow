from sqlalchemy import Column, String, Float, DateTime, Text, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timezone
from src.db.database import Base

class CropCycle(Base):
    __tablename__ = "crop_cycles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    crop_type = Column(String(100), nullable=False)
    variety = Column(String(100), nullable=True)
    planting_date = Column(DateTime(timezone=True), nullable=False)
    expected_harvest_date = Column(DateTime(timezone=True), nullable=True)
    actual_harvest_date = Column(DateTime(timezone=True), nullable=True)
    growth_stage = Column(String(50), default="seedling")
    yield_kg = Column(Float, nullable=True)
    quality_grade = Column(String(10), nullable=True)
    total_cost = Column(Float, default=0.0)
    revenue = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class YieldPrediction(Base):
    __tablename__ = "yield_predictions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    predicted_yield_kg = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=False)
    model_version = Column(String(50), nullable=False)
    prediction_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class PestDetection(Base):
    __tablename__ = "pest_detections"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    detection_type = Column(String(50), nullable=False)
    pest_name = Column(String(200), nullable=True)
    severity = Column(String(20), default="low")
    confidence_score = Column(Float, nullable=False)
    recommended_action = Column(Text, nullable=True)
    detected_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
