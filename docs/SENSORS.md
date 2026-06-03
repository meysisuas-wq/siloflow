# Sensor Integration Guide

## Supported Types
| Type | Unit | Range |
|------|------|-------|
| soil_moisture | % | 0-100 |
| temperature | C | -50 to 60 |
| humidity | % | 0-100 |
| light | lux | 0-120000 |
| soil_ph | pH | 0-14 |
| soil_nitrogen | ppm | 0-1000 |

## Sending Data
```bash
curl -X POST http://localhost:8001/api/v1/sensors/readings \
  -H "Content-Type: application/json" \
  -d '{"field_id":"uuid","sensor_id":"SOIL-001","sensor_type":"soil_moisture","value":45.2,"unit":"%"}'
```
