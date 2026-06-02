from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import structlog

logger = structlog.get_logger()

GROWTH_STAGES = {
    "rice": {"seedling": 15, "vegetative": 45, "flowering": 20, "fruiting": 25, "mature": 15},
    "corn": {"seedling": 14, "vegetative": 35, "flowering": 10, "fruiting": 35, "mature": 14},
    "wheat": {"seedling": 21, "vegetative": 60, "flowering": 14, "fruiting": 30, "mature": 14},
}

class GrowthTracker:
    def get_current_stage(self, crop_type: str, planting_date: datetime) -> Dict[str, Any]:
        stages = GROWTH_STAGES.get(crop_type, GROWTH_STAGES["rice"])
        days = (datetime.now(timezone.utc) - planting_date).days
        cumulative = 0
        for stage, duration in stages.items():
            cumulative += duration
            if days <= cumulative:
                progress = (days - (cumulative - duration)) / duration
                return {"stage": stage, "days_in_stage": days - (cumulative - duration),
                        "stage_duration_days": duration, "progress_pct": round(min(1.0, progress) * 100, 1),
                        "total_days_elapsed": days}
        return {"stage": "harvested", "progress_pct": 100, "total_days_elapsed": days}

    def predict_harvest_date(self, crop_type: str, planting_date: datetime) -> Optional[datetime]:
        stages = GROWTH_STAGES.get(crop_type, GROWTH_STAGES["rice"])
        return planting_date + timedelta(days=sum(stages.values()))

growth_tracker = GrowthTracker()
