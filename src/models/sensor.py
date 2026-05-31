from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime, timezone
from src.db.database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    sensor_id = Column(String(100), nullable=False, index=True)
    sensor_type = Column(String(50), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    quality_score = Column(Float, default=1.0)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    metadata = Column(JSONB, default=dict)

class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    source = Column(String(50), nullable=False)
    temperature_c = Column(Float, nullable=True)
    humidity_pct = Column(Float, nullable=True)
    wind_speed_kmh = Column(Float, nullable=True)
    rainfall_mm = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
