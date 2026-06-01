from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class FieldCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    crop_type: Optional[str] = None
    area_hectares: float = Field(..., gt=0)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None
    planting_date: Optional[datetime] = None

class FieldResponse(BaseModel):
    id: UUID
    name: str
    crop_type: Optional[str]
    area_hectares: float
    latitude: float
    longitude: float
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class SensorReadingCreate(BaseModel):
    field_id: UUID
    sensor_id: str
    sensor_type: str
    value: float
    unit: str

class SensorReadingResponse(BaseModel):
    id: UUID
    field_id: UUID
    sensor_id: str
    sensor_type: str
    value: float
    unit: str
    timestamp: datetime
    class Config:
        from_attributes = True

class YieldPredictionResponse(BaseModel):
    id: UUID
    field_id: UUID
    predicted_yield_kg: float
    confidence_score: float
    model_version: str
    prediction_date: datetime
    class Config:
        from_attributes = True

class DashboardSummary(BaseModel):
    total_fields: int
    total_area_hectares: float
    active_crops: int
    pending_alerts: int
    avg_soil_moisture: float
    avg_temperature: float
