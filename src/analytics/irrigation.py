from typing import Dict, Any, List
import structlog

logger = structlog.get_logger()

CROP_WATER = {"rice": {"seedling": 4, "vegetative": 6, "flowering": 8, "fruiting": 7, "mature": 4},
              "corn": {"seedling": 3, "vegetative": 5, "flowering": 7, "fruiting": 6, "mature": 3}}

class IrrigationOptimizer:
    async def calculate_schedule(self, field_data: Dict, sensor_data: List[Dict], weather: List[Dict]) -> Dict[str, Any]:
        crop = field_data.get("crop_type", "rice")
        stage = field_data.get("growth_stage", "vegetative")
        area = field_data.get("area_hectares", 1)
        irrigation_type = field_data.get("irrigation_type", "drip")

        moisture = [s["value"] for s in sensor_data if s.get("sensor_type") == "soil_moisture"]
        current = sum(moisture) / len(moisture) if moisture else 50

        daily_need = CROP_WATER.get(crop, CROP_WATER["rice"]).get(stage, 5)
        expected_rain = sum(f.get("precipitation_mm", 0) for f in weather[:3])
        irrigation_mm = max(0, daily_need - expected_rain)
        volume = irrigation_mm * area * 10

        efficiency = {"drip": 0.9, "sprinkler": 0.75, "flood": 0.5}
        actual_volume = volume / efficiency.get(irrigation_type, 0.8)

        return {"should_irrigate": irrigation_mm > 0, "irrigation_mm": round(irrigation_mm, 2),
                "volume_liters": round(actual_volume, 2), "current_moisture_pct": round(current, 1),
                "optimal_moisture_pct": 60, "expected_rain_mm": round(expected_rain, 2),
                "best_time": "early morning (05:00-07:00)" if irrigation_mm > 0 else None}

irrigation_optimizer = IrrigationOptimizer()
