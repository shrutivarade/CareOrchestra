# CareOrchestra Frontend

Placeholder for future web/mobile frontend.

## Purpose

This folder will contain user-facing applications for:

- **Provider Dashboard** - Doctor view of patient alerts, vitals, recommendations
- **Patient App** - Patient view of medications, appointments, vitals tracking
- **Nurse Interface** - Nurse handoff and shift management

## Planned Technology

- **Framework**: Streamlit (initial) or React (future)
- **State Management**: TBD
- **Authentication**: Google OAuth2
- **Styling**: TBD

## Planned Features

### Provider Dashboard
- Patient list with risk levels
- Alerts and escalations
- Vital trends visualization
- Medication adherence tracking
- Action recommendations

### Patient App
- Medication reminders
- Vitals tracking
- Appointment calendar
- Alert notifications
- Health summary

### Nurse Interface
- Patient handoff notes
- Pending actions
- Vital monitoring
- Status updates

## Implementation

Planned for Phase 3 of development.

Currently, the system operates headless via Python API.

## API Integration

Frontend will communicate with backend via REST API endpoints in `apps/api/`.

## Testing

Frontend testing will use:
- Streamlit app testing (for Streamlit version)
- Jest + React Testing Library (for React version)

## Deployment

- **Streamlit**: Streamlit Cloud or similar
- **React**: Vercel, Netlify, or GCS
- **Mobile**: React Native or Flutter (future)
