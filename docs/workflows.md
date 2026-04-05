# CareOrchestra Workflows

## Core Workflows

### Workflow 1: High Blood Pressure Alert

**Trigger**: Vitals input shows BP 165/100

**Flow**:
```
1. Monitoring Agent
   - Detects vitals input event
   - Validates data format
   - Retrieves patient context (age, conditions, history)
   ↓
2. Coordinator Agent
   - Receives enriched event
   - Determines this needs vitals analysis
   ↓
3. Vitals Agent
   - Queries recent BP history (last 30 days)
   - Applies BP rules (Stage 2 Hypertension threshold: 140+)
   - Analyzes trend (worsening, stable, improving)
   - Returns: HIGH RISK finding
   ↓
4. Coordinator Agent
   - In parallel: Requests medication check
   
5. Medication Agent
   - Checks if patient on antihypertensives
   - Checks last 7 days adherence
   - Returns: 60% adherence (missing doses)
   ↓
6. Coordinator Agent
   - Routes to Analysis Agent
   
7. Analysis Agent
   - Synthesizes: High BP + Poor medication adherence = HIGH RISK
   - Generates recommendations:
     a. Send medication reminder
     b. Escalate to patient's doctor
   ↓
8. Escalation Agent
   - Identifies patient's primary care doctor
   - Formats alert
   - Sends via Gmail
   - Records escalation in database
   ↓
9. Reporting Agent
   - Creates doctor summary
   - Includes: Current vitals, trend, med adherence, recommendations
```

**Expected Duration**: < 10 seconds
**Potential Actions**:
- Medication reminder sent to patient
- Doctor alert sent
- Appointment scheduled for follow-up

---

### Workflow 2: Missed Medication Detection

**Trigger**: Medication dose due (e.g., insulin injection at 8 AM)

**Flow**:
```
1. Monitoring Agent
   - Runs scheduled check for due medications
   - Detects patient didn't log insulin dose by 8:30 AM
   - Creates "medication_missed" event
   ↓
2. Coordinator Agent
   - Receives missed medication event
   ↓
3. Medication Agent
   - Confirms: Insulin dose was due, not logged within 30 min grace period
   - Checks: Is this a critical medication? YES (insulin for diabetes)
   - Checks: Recent adherence pattern? 70% (some misses)
   - Returns: CRITICAL MEDICATION MISSED
   ↓
4. Analysis Agent
   - Assesses: Missed insulin = high risk for hyperglycemia
   - Risk level: MODERATE to HIGH (depends on diabetes type)
   - Recommendations:
     a. URGENT: Patient reminder
     b. If pattern continues: Doctor escalation
   ↓
5. Coordinator Agent
   - Severity = MODERATE
   - Takes action: Send urgent reminder to patient
   - Option: Schedule follow-up call to patient
```

**Expected Duration**: < 5 seconds
**Patient Actions**: Usually resolved by patient taking dose after reminder

---

### Workflow 3: Appointment Follow-up

**Trigger**: Patient has appointment scheduled for 3 days out

**Flow**:
```
1. Monitoring Agent
   - Runs appointment check
   - Finds appointment due in 3 days
   ↓
2. Coordinator Agent
   - Routes to Scheduler Service
   
3. Scheduler Service
   - Gets appointment details
   - Checks patient vitals since last visit
   - Returns: Need vitals check before appointment
   ↓
4. Coordinator Agent
   - Requests Vitals Agent analysis
   - Requests Medication Agent check
   
   (Parallel agents)
   ↓
5. Analysis Agent
   - Diagnoses: Patient should have vitals checked before appointment
   - Medications on track
   ↓
6. Coordinator Agent
   - Decision: Send appointment reminder to patient
   - Include: "Please prepare vitals (BP, weight)" for appointment
   ↓
7. Reporting Agent
   - Creates pre-visit summary for doctor
   - Includes recent vitals, medication status
   - Sends to doctor's inbox pre-visit
```

**Expected Duration**: < 10 seconds
**Actions**: Reminder email/SMS, doctor gets summary before visit

---

### Workflow 4: Trend Warning (Declining Heart Rate)

**Trigger**: Heart rate trending down over last 7 days (120→90→70→60)

**Flow**:
```
1. Monitoring Agent
   - Runs daily trend check
   - Detects heart rate trending down consistently
   ↓
2. Coordinator Agent
   - Routes to Vitals Agent
   
3. Vitals Agent
   - Queries: Last 30 days of heart rate
   - Calculates: 7-day trend = -10 bpm/day
   - Threshold check: Normal HR is 60-100, current 60 at lower edge
   - BUT trends show progressive decline = CONCERNING
   - Risk assessment: MODERATE (could indicate medication side effect or other issue)
   ↓
4. Analysis Agent
   - Considers:
     - Patient on beta-blockers? (can lower HR)
     - Recent medication changes?
     - Other symptoms reported?
   - Recommendation: Doctor should review
   ↓
5. Escalation Agent
   - Creates alert: "Patient trend alert for MD review"
   - Sends to doctor
   - Does NOT auto-escalate (not immediately critical)
```

**Expected Duration**: < 10 seconds
**Doctor Action**: Review, adjust medication if needed

---

## Data Loading Workflow (Initial Setup)

**Flow**:
```
1. Run infra/scripts/load_seed_data.py
   - Reads data/seed/*.csv files
   - Parses patient records
   - Creates BigQuery tables
   ↓
2. Load patients.csv → patients table
   - Sample: 5 patient records
   ↓
3. Load vitals.csv → vitals table
   - Sample: 2 months history for each patient
   - Includes normal and abnormal readings
   ↓
4. Load medications.csv → medications table
   - Sample: Active medications for each patient
   ↓
5. Load medication_logs.csv → medication_logs table
   - Sample: Adherence data (some doses missed)
   ↓
6. Create mock_payloads
   - high_bp_event.json
   - missed_medication.json
   - followup_needed.json
   ↓
7. Ready for demo/testing
```

---

## Testing Workflows

### Unit Test: Vitals Rule Engine
```
Test: BP rule assessment
Input: systolic=160, diastolic=100
Expected: HIGH_RISK
Actual: Stage 2 hypertension flagged ✓
```

### Integration Test: Event Processing
```
Trigger: high_bp_event.json
Step 1: Load event
Step 2: Process through Coordinator
Step 3: Verify Vitals Agent called
Step 4: Verify Analysis Agent called
Step 5: Verify alert created
```

### E2E Test: Full Escalation Flow
```
Setup: Mock patient data loaded
Action: Inject critical vitals event
Expected: 
  - Alert created
  - Doctor email sent (mock)
  - Escalation recorded
  - Report generated
Verify: All steps completed < 15 seconds
```

---

## Future Workflow Enhancements

- Lab result processing workflow
- Symptom checker workflow
- Insurance/billing verification workflow
- Complex multi-condition risk assessment workflow
- Population health trending workflow
