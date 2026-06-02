import asyncio
from datetime import datetime, timezone
from uuid import uuid4
from src.db.database import init_db, async_session
from src.models.field import Field

async def seed():
    await init_db()
    async with async_session() as db:
        fields = [
            Field(name="North Paddy Field", farmer_id=uuid4(), crop_type="rice", area_hectares=2.5,
                  latitude=-6.2088, longitude=106.8456, soil_type="clay_loam", irrigation_type="flood",
                  planting_date=datetime(2026, 4, 1, tzinfo=timezone.utc)),
            Field(name="South Corn Plot", farmer_id=uuid4(), crop_type="corn", area_hectares=1.8,
                  latitude=-6.2100, longitude=106.8470, soil_type="sandy_loam", irrigation_type="drip",
                  planting_date=datetime(2026, 4, 15, tzinfo=timezone.utc)),
        ]
        db.add_all(fields)
        await db.commit()
        print(f"Seeded {len(fields)} fields!")

if __name__ == "__main__":
    asyncio.run(seed())
