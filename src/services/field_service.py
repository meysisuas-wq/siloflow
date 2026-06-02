from typing import Dict, Any, List, Optional
from uuid import UUID
import structlog
from src.models.field import Field

logger = structlog.get_logger()

class FieldService:
    async def create_field(self, db, data: dict) -> Field:
        field = Field(name=data["name"], farmer_id=data["farmer_id"], crop_type=data.get("crop_type"),
                      area_hectares=data["area_hectares"], latitude=data["latitude"], longitude=data["longitude"],
                      soil_type=data.get("soil_type"), irrigation_type=data.get("irrigation_type"))
        db.add(field)
        await db.flush()
        logger.info("field_created", field_id=str(field.id), name=field.name)
        return field

    async def get_field(self, db, field_id: UUID) -> Optional[Field]:
        return await db.get(Field, field_id)

    async def list_fields(self, db, farmer_id: UUID, crop_type: Optional[str] = None) -> List[Field]:
        from sqlalchemy import select
        q = select(Field).where(Field.farmer_id == farmer_id, Field.is_active == True)
        if crop_type: q = q.where(Field.crop_type == crop_type)
        result = await db.execute(q)
        return result.scalars().all()

field_service = FieldService()
