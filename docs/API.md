# SiloFlow API Reference

## Base URL
`http://localhost:8001/api/v1`

## Endpoints

### Fields
- POST /fields — Create field
- GET /fields — List fields
- GET /fields/{id} — Get field

### Sensors
- POST /sensors/readings — Submit reading
- POST /sensors/readings/batch — Batch readings
- GET /sensors/{field_id}/readings — Get readings

### Predictions
- GET /predictions/yield/{field_id} — Yield predictions
- POST /predictions/yield/{field_id} — Request prediction

### Dashboard
- GET /dashboard — Summary data
