# CareOrchestra Demo Script

## Overview

This demo runs the CareOrchestra system end-to-end with mock data to demonstrate the multi-agent coordination workflow.

## Prerequisites

- Python 3.9+
- Google Cloud Project (or mock mode)
- BigQuery access (or mock data)
- Environment variables configured (.env)

## Quick Start

### 1. Setup Environment

```bash
# Create .env file from template
cp .env.example .env

# Edit .env to configure (mainly for GCP project)
# For demo with mock data, defaults should work
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Load Mock Data

```bash
python infra/scripts/load_seed_data.py
```

This will:
- Create BigQuery tables
- Load patient records from `data/seed/patients.csv`
- Load vitals history from `data/seed/vitals.csv`
- Load medications from `data/seed/medications.csv`
- Load medication logs from adherence data
- Create sample appointments and followups

### 4. Run the Application

```bash
# From project root
python -m apps.adk_app.app

# Or use the main entry point script (if created)
python apps/adk_app/app.py
```

---

## Demo Scenarios

### Scenario 1: High Blood Pressure Alert

**Setup**: Patient with hypertension has elevated BP reading

**File**: `data/mock_payloads/high_bp_event.json`

```json
{
  "event_type": "vitals_submitted",
  "patient_id": "PT001",
  "vital_type": "blood_pressure",
  "systolic": 165,
  "diastolic": 100,
  "measured_at": "2025-04-05T14:30:00Z"
}
```

**Expected Flow**:
1. Monitoring Agent detects vitals event
2. Coordinator routes to Vitals Agent
3. Vitals Agent: Identifies Stage 2 Hypertension (HIGH RISK)
4. Medication Agent: Finds patient on antihypertensive with poor adherence
5. Analysis Agent: Synthesizes → HIGH RISK (high BP + poor med adherence)
6. Escalation Agent: Sends alert to doctor
7. Reporting Agent: Creates summary

**Expected Output**:
- Alert created in database
- Doctor email sent (mock or real)
- Medication reminder sent to patient
- Report generated for doctor review

---

### Scenario 2: Missed Medication

**Setup**: Patient missed insulin injection

**File**: `data/mock_payloads/missed_medication.json`

```json
{
  "event_type": "medication_check",
  "patient_id": "PT003",
  "medication_id": "MED003",
  "scheduled_time": "2025-04-05T08:00:00Z",
  "grace_period_minutes": 30
}
```

**Expected Flow**:
1. Monitoring Agent: Detects scheduled medication check
2. Coordinator routes to Medication Agent
3. Medication Agent: Confirms dose not logged within grace period
4. Medication Agent: Flags CRITICAL (insulin is critical medication)
5. Analysis Agent: Assesses HIGH RISK for hyperglycemia
6. Coordinator: Routes to escalation (critical med missed)
7. Escalation Agent: May send urgent alert to patient or doctor

**Expected Output**:
- Urgent reminder to patient
- Alert to doctor if pattern detected
- Dose logged as missed in database

---

### Scenario 3: Appointment Follow-up

**Setup**: Patient has appointment in 3 days

**File**: `data/mock_payloads/followup_needed.json`

```json
{
  "event_type": "appointment_upcoming",
  "patient_id": "PT002",
  "appointment_id": "APT001",
  "scheduled_at": "2025-04-08T10:00:00Z",
  "days_until": 3
}
```

**Expected Flow**:
1. Monitoring Agent: Detects upcoming appointment
2. Coordinator: Routes to Vitals and Medication Agents
3. Vitals Agent: Gathers recent vitals for context
4. Medication Agent: Checks current med status
5. Reporting Agent: Creates pre-visit summary for doctor
6. Scheduler Service: Sends appointment reminder to patient
7. Optional: Requests vitals check before appointment

**Expected Output**:
- Appointment reminder to patient
- Pre-visit summary to doctor
- Any urgent pre-visit findings flagged

---

## Integration Testing

### Test 1: End-to-End Event Processing

```python
# tests/e2e/test_high_bp_workflow.py
async def test_high_bp_alert_flow():
    """Test complete flow for high BP alert."""
    # Setup
    event = load_mock_event("data/mock_payloads/high_bp_event.json")
    
    # Execute
    action = await app.process_event(event)
    
    # Verify
    assert action['alert_created'] == True
    assert action['escalated'] == True
    assert action['doctor_notified'] == True
```

### Test 2: Agent Coordination

```python
# tests/unit/test_coordinator.py
async def test_coordinator_delegates_correctly():
    """Test coordinator routes to correct agents."""
    coordinator = CoordinatorAgent()
    event = {
        'type': 'vitals_submitted',
        'vital_type': 'blood_pressure'
    }
    result = await coordinator.coordinate(event)
    assert result['vitals_agent_called'] == True
```

### Test 3: Risk Rules

```python
# tests/unit/test_vitals_rules.py
def test_high_bp_risk_assessment():
    """Test vital risk rule engine."""
    from apps.adk_app.tools.risk_rules.vitals_rules import VitalsRulesEngine
    
    result = VitalsRulesEngine.assess_blood_pressure(
        systolic=165,
        diastolic=100
    )
    assert result['risk_level'] == 'high'
    assert 'Stage 2 Hypertension' in result['findings']
```

---

## Running with Real Data

Once integrated with real BigQuery:

1. Update `.env` with real GCP project
2. Configure real patient data in BigQuery
3. Set `USE_MOCK_DATA=false` in `.env`
4. Configure real Gmail and Calendar credentials
5. Run: `python apps/adk_app/app.py`

The same code works with real data - no changes needed!

---

## Debugging

### Enable Debug Logging

```bash
# In .env
DEBUG=true
LOG_LEVEL=DEBUG
```

### Inspect Mock Data

```bash
# View sample events
cat data/mock_payloads/high_bp_event.json
cat data/mock_payloads/missed_medication.json

# View seed data
head -5 data/seed/patients.csv
head -5 data/seed/vitals.csv
```

### Test Individual Agents

```python
# Test vitals agent in isolation
from apps.adk_app.agents.vitals import VitalsAgent
agent = VitalsAgent()
result = await agent.analyze_vitals('PT001')
```

---

## Performance Baseline

Target metrics with demo data:

- Event processing: < 5 seconds
- Doctor alert delivery: < 10 seconds
- Report generation: < 2 seconds
- Database queries: < 1 second

---

## Next Steps

1. **Frontend**: Build Streamlit dashboard for provider/patient
2. **Real Integration**: Connect to actual EHR system
3. **ML Enhanced**: Add predictive models for risk scoring
4. **Scale Testing**: Run with 10,000+ patient population
5. **Compliance**: Add audit logging and encryption

---

## Sample Run Output

```
[INFO] Starting CareOrchestra
[INFO] Initializing agents
[INFO] Initializing services
[INFO] Initializing tools
[INFO] CareOrchestra initialized successfully

[INFO] Processing event: vitals_submitted
[INFO] Loading patient PT001
[INFO] Vitals Agent: Analyzing blood pressure 165/100
[INFO] Vitals Agent: HIGH RISK - Stage 2 Hypertension
[INFO] Medication Agent: Checking adherence
[INFO] Medication Agent: 60% adherence (missing doses)
[INFO] Analysis Agent: Synthesizing findings
[INFO] Analysis Agent: Risk Level = HIGH
[INFO] Escalation Agent: Sending alert to doctor
[MOCK] Sending alert email to doctor@clinic.com
[INFO] Reporting Agent: Generating summary
[INFO] Action complete - Escalation sent to doctor

Status: SUCCESS
```
