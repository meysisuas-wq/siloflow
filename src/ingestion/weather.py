from typing import Dict, Any, List
from datetime import datetime, timezone
import httpx, structlog

logger = structlog.get_logger()

class WeatherService:
    def __init__(self):
        self._client = httpx.AsyncClient(timeout=30.0)

    async def get_current_weather(self, lat: float, lng: float) -> Dict[str, Any]:
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {"latitude": lat, "longitude": lng,
                      "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,rain,cloud_cover",
                      "timezone": "auto"}
            r = await self._client.get(url, params=params)
            r.raise_for_status()
            c = r.json().get("current", {})
            return {"temperature_c": c.get("temperature_2m"), "humidity_pct": c.get("relative_humidity_2m"),
                    "wind_speed_kmh": c.get("wind_speed_10m"), "rainfall_mm": c.get("rain")}
        except Exception as e:
            logger.error("weather_fetch_failed", error=str(e))
            return {}

    async def get_forecast(self, lat: float, lng: float, days: int = 7) -> List[Dict]:
        try:
            r = await self._client.get("https://api.open-meteo.com/v1/forecast",
                params={"latitude": lat, "longitude": lng,
                        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                        "timezone": "auto", "forecast_days": days})
            r.raise_for_status()
            d = r.json().get("daily", {})
            return [{"date": d["time"][i], "temp_max": d["temperature_2m_max"][i],
                     "temp_min": d["temperature_2m_min"][i], "precipitation_mm": d["precipitation_sum"][i]}
                    for i in range(len(d.get("time", [])))]
        except Exception as e:
            logger.error("forecast_failed", error=str(e))
            return []

weather_service = WeatherService()
