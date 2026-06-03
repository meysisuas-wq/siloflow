# SiloFlow Architecture

## Data Flow
```
IoT Sensors → Ingestion Pipeline → TimescaleDB
Satellite API → Weather Service → Analytics Engine
    → ML Models (Yield, Pest, Irrigation) → Farmer Dashboard / Alerts
```

## Key Components
1. Data Ingestion Pipeline — Real-time sensor streams with validation
2. Analytics Engine — Time-series analysis, trend detection
3. ML Models — Yield prediction, pest detection, irrigation optimization
4. Alert System — Threshold-based automated monitoring
5. Growth Tracker — Crop lifecycle management

## Tech Stack
- Backend: FastAPI + SQLAlchemy
- Database: TimescaleDB (PostgreSQL)
- Cache: Redis
- ML: PyTorch + scikit-learn + XGBoost
- GPU: AMD ROCm for accelerated inference
