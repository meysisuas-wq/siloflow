from typing import Dict, Any, List
from datetime import datetime, timezone
from enum import Enum
import structlog

logger = structlog.get_logger()

class AlertType(str, Enum):
    FROST = "frost"
    DROUGHT = "drought"
    PEST = "pest"
    IRRIGATION = "irrigation"
    WEATHER = "weather"
    HARVEST_READY = "harvest_ready"

THRESHOLDS = {"frost_temp_c": 2.0, "heat_temp_c": 40.0, "low_moisture_pct": 20.0, "high_moisture_pct": 85.0}

class AlertManager:
    async def evaluate_conditions(self, field_data: Dict, sensor_data: List[Dict], weather: Dict) -> List[Dict]:
        alerts = []
        temp = weather.get("temperature_c")
        if temp is not None and temp <= THRESHOLDS["frost_temp_c"]:
            alerts.append({"type": AlertType.FROST.value, "severity": "critical",
                           "message": f"Frost risk: {temp}C", "field_id": str(field_data.get("id"))})

        moisture = [s["value"] for s in sensor_data if s.get("sensor_type") == "soil_moisture"]
        if moisture:
            avg = sum(moisture) / len(moisture)
            if avg < THRESHOLDS["low_moisture_pct"]:
                alerts.append({"type": AlertType.DROUGHT.value, "severity": "warning",
                               "message": f"Low moisture: {avg:.1f}%", "field_id": str(field_data.get("id"))})
        return alerts

alert_manager = AlertManager()
