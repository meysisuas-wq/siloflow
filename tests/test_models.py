import pytest
from src.models.yield_predictor import YieldPredictor
from src.models.pest_detector import PEST_DATABASE
from src.analytics.growth_tracker import growth_tracker, GROWTH_STAGES
from src.analytics.timeseries import TimeSeriesAnalyzer
from datetime import datetime, timezone

class TestYieldPredictor:
    def test_base_yields(self):
        p = YieldPredictor()
        assert p._moisture_factor(55) == 1.0
        assert p._moisture_factor(10) == 0.6
        assert p._temp_factor(25) == 1.0

class TestPestDetector:
    def test_pest_database(self):
        assert "rice_blast" in PEST_DATABASE
        assert "corn" in PEST_DATABASE["fall_armyworm"]["crops"]

class TestGrowthTracker:
    def test_current_stage(self):
        result = growth_tracker.get_current_stage("rice", datetime(2026, 4, 1, tzinfo=timezone.utc))
        assert "stage" in result
        assert "progress_pct" in result

    def test_predict_harvest(self):
        h = growth_tracker.predict_harvest_date("rice", datetime(2026, 4, 1, tzinfo=timezone.utc))
        assert h is not None
        assert h > datetime(2026, 4, 1, tzinfo=timezone.utc)

class TestTimeSeries:
    def test_trend_increasing(self):
        import asyncio
        r = asyncio.run(TimeSeriesAnalyzer().detect_trend([1,2,3,4,5,6,7,8,9,10]))
        assert r["trend"] == "increasing"

    def test_anomalies(self):
        import asyncio
        r = asyncio.run(TimeSeriesAnalyzer().detect_anomalies([50,51,49,50,51,100,49,50]))
        assert any(a["value"] == 100 for a in r)
