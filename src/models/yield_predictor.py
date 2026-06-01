from typing import Dict, Any, List
import numpy as np, structlog

logger = structlog.get_logger()

BASE_YIELDS = {"rice": 5.5, "wheat": 3.5, "corn": 6.0, "soybean": 2.5, "cassava": 15.0, "potato": 25.0}

class YieldPredictor:
    def __init__(self):
        self._model_version = "1.0.0"

    async def predict(self, field_data: Dict, sensor_data: List[Dict]) -> Dict[str, Any]:
        crop = field_data.get("crop_type", "rice")
        area = field_data.get("area_hectares", 1)
        base = BASE_YIELDS.get(crop, 4.0)

        moisture = [s["value"] for s in sensor_data if s.get("sensor_type") == "soil_moisture"]
        temps = [s["value"] for s in sensor_data if s.get("sensor_type") == "temperature"]
        nitrogen = [s["value"] for s in sensor_data if s.get("sensor_type") == "soil_nitrogen"]

        moisture_factor = self._moisture_factor(np.mean(moisture) if moisture else 50)
        temp_factor = self._temp_factor(np.mean(temps) if temps else 25)
        nutrient_factor = 0.9 if nitrogen and np.mean(nitrogen) > 100 else 0.7

        predicted = base * area * moisture_factor * temp_factor * nutrient_factor
        confidence = min(0.95, 0.5 + (1 if moisture else 0) * 0.15 + (1 if temps else 0) * 0.15 + (1 if nitrogen else 0) * 0.15)

        return {"predicted_yield_kg": round(predicted, 2),
                "confidence_interval_low": round(predicted * 0.85, 2),
                "confidence_interval_high": round(predicted * 1.15, 2),
                "confidence_score": round(confidence, 3),
                "model_version": self._model_version}

    def _moisture_factor(self, m: float) -> float:
        if 40 <= m <= 70: return 1.0
        elif 30 <= m <= 80: return 0.85
        return 0.6

    def _temp_factor(self, t: float) -> float:
        if 20 <= t <= 35: return 1.0
        elif 15 <= t <= 40: return 0.9
        return 0.7

yield_predictor = YieldPredictor()
