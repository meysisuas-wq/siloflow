from typing import Dict, Any, List
import numpy as np, structlog

logger = structlog.get_logger()

class TimeSeriesAnalyzer:
    async def detect_trend(self, values: List[float]) -> Dict[str, Any]:
        if len(values) < 3:
            return {"trend": "insufficient_data", "slope": 0}
        x = np.arange(len(values))
        coeffs = np.polyfit(x, values, 1)
        slope = coeffs[0]
        direction = "increasing" if slope > 0.5 else "decreasing" if slope < -0.5 else "stable"
        return {"trend": direction, "slope": round(float(slope), 4),
                "mean": round(float(np.mean(values)), 2), "std": round(float(np.std(values)), 2)}

    async def detect_anomalies(self, values: List[float], threshold: float = 2.0) -> List[Dict]:
        if len(values) < 5: return []
        mean, std = np.mean(values), np.std(values)
        if std == 0: return []
        return [{"index": i, "value": round(v, 2), "z_score": round(abs((v - mean) / std), 2),
                 "type": "high" if v > mean else "low"} for i, v in enumerate(values) if abs((v - mean) / std) > threshold]

    async def forecast_simple(self, values: List[float], periods: int = 7) -> List[Dict]:
        if len(values) < 3: return []
        ma = np.mean(values[-7:])
        std = np.std(values[-7:])
        return [{"period": i + 1, "forecast": round(float(ma + np.random.normal(0, std * 0.1)), 2)}
                for i in range(periods)]

timeseries_analyzer = TimeSeriesAnalyzer()
