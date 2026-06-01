from typing import Dict, Any, List, Optional
import structlog

logger = structlog.get_logger()

PEST_DATABASE = {
    "rice_blast": {"name": "Rice Blast", "severity": "medium", "crops": ["rice"],
                   "treatment": "Apply fungicide (tricyclazole). Improve drainage."},
    "brown_planthopper": {"name": "Brown Planthopper", "severity": "high", "crops": ["rice"],
                          "treatment": "Use resistant varieties. Apply imidacloprid if severe."},
    "fall_armyworm": {"name": "Fall Armyworm", "severity": "high", "crops": ["corn", "rice"],
                      "treatment": "Apply chlorantraniliprole or emamectin benzoate."},
    "late_blight": {"name": "Late Blight", "severity": "critical", "crops": ["potato"],
                    "treatment": "Apply metalaxyl + mancozeb. Remove infected plants."},
}

class PestDetector:
    async def detect_from_image(self, image_data: bytes, crop_type: str) -> Dict[str, Any]:
        import random
        detections = []
        for pid, info in PEST_DATABASE.items():
            if crop_type in info["crops"] and random.random() > 0.7:
                detections.append({"pest_id": pid, "name": info["name"],
                    "confidence": round(random.uniform(0.6, 0.98), 3),
                    "severity": info["severity"], "recommended_action": info["treatment"]})
        detections.sort(key=lambda x: x["confidence"], reverse=True)
        return {"detections": detections, "has_threats": any(d["confidence"] > 0.7 for d in detections)}

    async def list_pests_for_crop(self, crop_type: str) -> List[Dict]:
        return [{"id": pid, **info} for pid, info in PEST_DATABASE.items() if crop_type in info["crops"]]

pest_detector = PestDetector()
