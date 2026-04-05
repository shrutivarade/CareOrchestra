# CareOrchestra API

Placeholder for future FastAPI REST wrapper.

## Purpose

This folder will contain a FastAPI wrapper around the core ADK agents, providing:

- REST API endpoints for patient data and event submission
- Integration with frontend applications
- Request validation and authentication
- Response formatting and documentation

## Planned Endpoints

- `POST /api/v1/events` - Submit patient events
- `GET /api/v1/patients/{patient_id}` - Get patient info
- `GET /api/v1/vitals/{patient_id}` - Get recent vitals
- `POST /api/v1/vitals` - Record vital reading
- `GET /api/v1/medications/{patient_id}` - Get medication schedule
- `POST /api/v1/medications/{patient_id}/log` - Log medication dose
- `GET /api/v1/alerts/{patient_id}` - Get recent alerts
- `GET /api/v1/appointments/{patient_id}` - Get appointments

## Implementation

Planned for Phase 2 of development.

Currently using direct Python API from ADK application.

## Testing

API testing will use pytest with FastAPI TestClient.

See `/tests/` for test structure.
