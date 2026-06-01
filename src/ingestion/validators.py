from typing import Dict, Any
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger()

SENSOR_RANGES = {
    "soil_moisture": {"min": 0, "max": 100, "unit": "%"},
    "temperature": {"min": -50, "max": 60, "unit": "C"},
    "humidity": {"min": 0, "max": 100, "unit": "%"},
    "light": {"min": 0, "max": 120000, "unit": "lux"},
    "wind_speed": {"min": 0, "max": 200, "unit": "km/h"},
    "rainfall": {"min": 0, "max": 500, "unit": "mm"},
    "soil_ph": {"min": 0, "max": 14, "unit": "pH"},
    "soil_nitrogen": {"min": 0, "max": 1000, "unit": "ppm"},
}

async def validate_sensor_reading(data: Dict[str, Any]) -> bool:
    sensor_type = data.get("sensor_type")
    value = data.get("value")
    if sensor_type is None or value is None: return False
    r = SENSOR_RANGES.get(sensor_type)
    if r and not (r["min"] <= value <= r["max"]):
        logger.warning("value_out_of_range", sensor_type=sensor_type, value=value)
        return False
    return True

async def validate_timestamp(data: Dict[str, Any]) -> bool:
    if data.get("timestamp") is None:
        data["timestamp"] = datetime.now(timezone.utc).isoformat()
    return True
