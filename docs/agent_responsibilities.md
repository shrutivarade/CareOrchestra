# Agent Responsibilities

## 1. Coordinator Agent
**File**: `agents/coordinator.py`

### Primary Responsibility
Main orchestrator that receives events and delegates analysis to specialist agents, then synthesizes results into a final care action.

### Key Responsibilities
- Receive patient events from monitoring agent
- Delegate vital analysis to Vitals Agent
- Delegate medication checks to Medication Agent
- Route findings to Analysis Agent
- Receive recommendations from Analysis Agent
- Make final decision on action (reminder, alert, escalation)
- Route high-risk cases to Escalation Agent

### Inputs
- Patient event (vitals update, medication reminder due, appointment follow-up, etc.)
- Patient ID

### Outputs
- Recommended action (medication reminder, vitals check request, escalation trigger)
- Confidence level/reasoning

### Success Metrics
- Response latency < 5 seconds
- Correct escalation decisions 95%+ accuracy

---

## 2. Monitoring Agent
**File**: `agents/monitoring.py`

### Primary Responsibility
Watches for patient-related events and triggers downstream analysis.

### Key Responsibilities
- Poll for scheduled events (medication times, appointments)
- Process incoming vitals submissions
- Detect manual alerts/entries from patient
- Route all events to Coordinator Agent
- Enrich events with patient context before routing

### Inputs
- Scheduled events (from database)
- Manual patient entries
- External event triggers

### Outputs
- Enriched events routed to Coordinator Agent

### Success Metrics
- Detects 100% of scheduled events
- Event latency < 1 minute
- Handles 1000+ concurrent patient streams

---

## 3. Vitals Agent
**File**: `agents/vitals.py`

### Primary Responsibility
Analyzes vital signs for abnormal values, trends, and patterns.

### Key Responsibilities
- Query recent vital history for patient
- Apply vital sign rules (BP ranges, HR ranges, glucose targets, SpO2 levels)
- Detect abnormal individual values
- Identify concerning trends (rising BP, falling oxygen, etc.)
- Compare against patient baseline and condition expectations
- Flag critical values

### Vital Types Tracked
- Blood Pressure (systolic/diastolic)
- Heart Rate
- Blood Glucose
- Oxygen Saturation (SpO2)
- Temperature
- Weight

### Inputs
- Patient ID
- Recent vital readings (from BigQuery)

### Outputs
- Vital analysis findings (normal, abnormal, critical)
- Trend assessment
- Risk flags

### Success Metrics
- Correctly identifies abnormal vitals 98%+ accuracy
- Detects dangerous trends within 24 hours

---

## 4. Medication Agent
**File**: `agents/medication.py`

### Primary Responsibility
Tracks medication adherence and flags compliance issues.

### Key Responsibilities
- Query active medications for patient
- Pull medication logs for adherence tracking
- Identify missed doses
- Calculate adherence percentage
- Flag critical medication misses (anticoagulants, insulin, etc.)
- Suggest reminder timing
- Detect medication changes needing follow-up

### Inputs
- Patient ID
- Medication schedule
- Medication logs

### Outputs
- Adherence status (excellent/good/fair/poor)
- Missed dose alerts
- Adherence trends

### Success Metrics
- Detects 99%+ of missed doses
- Suggests reminders that improve adherence 20%+

---

## 5. Analysis Agent
**File**: `agents/analysis.py`

### Primary Responsibility
Synthesizes data from multiple agents to produce comprehensive risk assessment.

### Key Responsibilities
- Receive vital findings from Vitals Agent
- Receive medication findings from Medication Agent
- Consider patient medical history
- Incorporate event context
- Assess composite risk level (low/moderate/high/critical)
- Generate prioritized recommendations
- Determine escalation pathway if needed

### Inputs
- Vitals analysis
- Medication analysis
- Patient history
- Event context

### Outputs
- Risk level classification
- Key findings summary
- Prioritized action recommendations
- Escalation recommendation (yes/no)

### Success Metrics
- Risk assessment accuracy > 90%
- Recommendations followed by 80%+ of patients
- False positive escalations < 5%

---

## 6. Escalation Agent
**File**: `agents/escalation.py`

### Primary Responsibility
Routes high-risk situations to appropriate healthcare providers.

### Key Responsibilities
- Identify high-risk situations requiring escalation
- Retrieve doctor/provider contact information
- Format alert for clinical consumption using formatter
- Send alert via Gmail
- Record escalation in database
- Handle escalation status tracking

### Inputs
- Alert data (findings, risk level, recommendations)
- Patient ID

### Outputs
- Escalation confirmation
- Delivery status

### Success Metrics
- Alert delivery success rate > 99%
- Doctor acknowledgment within 30 minutes (target)
- No lost escalations

---

## 7. Reporting Agent
**File**: `agents/reporting.py`

### Primary Responsibility
Creates clinical summaries and reports for healthcare providers and staff.

### Key Responsibilities
- Generate doctor summaries for scheduling/review
- Create nurse handoff reports for shift changes
- Produce vitals trend reports
- Generate medication reconciliation reports
- Create periodic patient summaries

### Inputs
- Patient ID
- Analysis results
- Vital history
- Medication history

### Outputs
- Formatted clinical reports
- Summaries optimized for audience

### Success Metrics
- Summaries generated < 1 minute
- Clinician feedback satisfaction > 4/5

---

## Agent Communication Patterns

### Synchronous Flow
```
Coordinator Agent
    ↓ (requests) → Vitals Agent (responds)
    ↓ (requests) → Medication Agent (responds)
    ↓ (requests) → Analysis Agent (responds)
    ↓ (routes) → Escalation Agent (if needed)
    ↓ (routes) → Reporting Agent (if needed)
```

### Event-Driven
```
Monitoring Agent → [Event] → Coordinator Agent → [Decision] → Action Agents
```

## Future Agent Ideas (Placeholder)

- **Symptom Checker Agent**: Analyzes patient-reported symptoms
- **Lab Agent**: Processes lab results and abnormalities
- **Comorbidity Agent**: Factors in interaction with other conditions
- **Insurance Agent**: Validates coverage and billing
- **Preventive Agent**: Suggests preventive care and screenings
