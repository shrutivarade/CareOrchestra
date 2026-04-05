# BigQuery Schema for CareOrchestra

## Dataset Configuration

**Dataset ID**: `care_orchestra` (configurable via `BIGQUERY_DATASET`)
**Location**: `us-central1` (configurable via `GCP_LOCATION`)
**Default Expiration**: 90 days for intermediate tables

---

## Core Tables

### 1. patients
**Purpose**: Patient information and metadata

**Schema**:
```sql
CREATE TABLE IF NOT EXISTS care_orchestra.patients (
  patient_id STRING NOT NULL,
  first_name STRING,
  last_name STRING,
  date_of_birth DATE,
  phone_number STRING,
  email STRING,
  conditions ARRAY<STRING>,  -- ['hypertension', 'diabetes', ...]
  care_team ARRAY<STRING>,   -- Doctor IDs
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  
  PRIMARY KEY (patient_id) NOT ENFORCED
);
```

**Example Row**:
```json
{
  "patient_id": "PT001",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1965-05-15",
  "phone_number": "(555) 123-4567",
  "email": "john.doe@email.com",
  "conditions": ["hypertension", "type2_diabetes"],
  "care_team": ["DR001"],
  "created_at": "2025-04-01 10:00:00 UTC",
  "updated_at": "2025-04-05 14:30:00 UTC"
}
```

---

### 2. vitals
**Purpose**: Vital sign readings

**Schema**:
```sql
CREATE TABLE IF NOT EXISTS care_orchestra.vitals (
  record_id STRING NOT NULL,
  patient_id STRING NOT NULL,
  vital_type STRING NOT NULL,  -- 'blood_pressure', 'heart_rate', 'glucose', 'spo2', 'temperature', 'weight'
  value FLOAT64,
  unit STRING,  -- 'mmHg', 'bpm', 'mg/dL', '%', 'F', 'lbs'
  systolic INT64,  -- For BP only
  diastolic INT64,  -- For BP only
  measured_at TIMESTAMP NOT NULL,
  notes STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  
  PRIMARY KEY (record_id) NOT ENFORCED,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id) NOT ENFORCED
);

CREATE INDEX idx_vitals_patient_type ON care_orchestra.vitals(patient_id, vital_type, measured_at);
```

**Example Rows**:
```json
{
  "record_id": "VIT001",
  "patient_id": "PT001",
  "vital_type": "blood_pressure",
  "value": null,
  "unit": "mmHg",
  "systolic": 165,
  "diastolic": 100,
  "measured_at": "2025-04-05 14:30:00 UTC",
  "notes": "Home measurement",
  "created_at": "2025-04-05 14:35:00 UTC"
}
```

---

### 3. medications
**Purpose**: Patient medication list

**Schema**:
```sql
CREATE TABLE IF NOT EXISTS care_orchestra.medications (
  medication_id STRING NOT NULL,
  patient_id STRING NOT NULL,
  name STRING NOT NULL,
  dosage STRING,  -- '500mg', '10 units'
  frequency STRING,  -- 'once daily', 'twice daily', 'as needed'
  route STRING,  -- 'oral', 'injection', 'topical'
  reason STRING,  -- 'hypertension', 'diabetes'
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP,
  notes STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  
  PRIMARY KEY (medication_id) NOT ENFORCED,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id) NOT ENFORCED
);
```

**Example Row**:
```json
{
  "medication_id": "MED001",
  "patient_id": "PT001",
  "name": "Lisinopril",
  "dosage": "10mg",
  "frequency": "once daily",
  "route": "oral",
  "reason": "hypertension",
  "start_date": "2024-01-15 00:00:00 UTC",
  "end_date": null,
  "notes": "ACE inhibitor for blood pressure",
  "created_at": "2024-01-15 10:00:00 UTC",
  "updated_at": "2025-04-01 00:00:00 UTC"
}
```

---

### 4. medication_logs
**Purpose**: Medication adherence tracking

**Schema**:
```sql
CREATE TABLE IF NOT EXISTS care_orchestra.medication_logs (
  log_id STRING NOT NULL,
  patient_id STRING NOT NULL,
  medication_id STRING NOT NULL,
  scheduled_time TIMESTAMP NOT NULL,
  actual_time TIMESTAMP,
  taken BOOLEAN DEFAULT FALSE,
  notes STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  
  PRIMARY KEY (log_id) NOT ENFORCED,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id) NOT ENFORCED,
  FOREIGN KEY (medication_id) REFERENCES medications(medication_id) NOT ENFORCED
);

CREATE INDEX idx_med_logs_patient_time ON care_orchestra.medication_logs(patient_id, scheduled_time);
```

**Example Row**:
```json
{
  "log_id": "LOG001",
  "patient_id": "PT001",
  "medication_id": "MED001",
  "scheduled_time": "2025-04-05 09:00:00 UTC",
  "actual_time": "2025-04-05 09:15:00 UTC",
  "taken": true,
  "notes": null,
  "created_at": "2025-04-05 09:15:00 UTC"
}
```

---

### 5. alerts
**Purpose**: System alerts and notifications

**Schema**:
```sql
CREATE TABLE IF NOT EXISTS care_orchestra.alerts (
  alert_id STRING NOT NULL,
  patient_id STRING NOT NULL,
  alert_type STRING NOT NULL,  -- 'vital_abnormal', 'medication_missed', 'appointment_due', 'trend_warning', 'critical_event'
  severity STRING NOT NULL,  -- 'low', 'moderate', 'high', 'critical'
  title STRING NOT NULL,
  description STRING NOT NULL,
  findings ARRAY<STRING>,
  recommendations ARRAY<STRING>,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  acknowledged BOOLEAN DEFAULT FALSE,
  acknowledged_by STRING,
  acknowledged_at TIMESTAMP,
  
  PRIMARY KEY (alert_id) NOT ENFORCED,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id) NOT ENFORCED
);

CREATE INDEX idx_alerts_patient_severity ON care_orchestra.alerts(patient_id, severity, created_at);
```

---

### 6. escalations
**Purpose**: Doctor alerts and escalation tracking

**Schema**:
```sql
CREATE TABLE IF NOT EXISTS care_orchestra.escalations (
  escalation_id STRING NOT NULL,
  alert_id STRING NOT NULL,
  patient_id STRING NOT NULL,
  provider_id STRING NOT NULL,
  provider_email STRING NOT NULL,
  alert_content STRING NOT NULL,
  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  delivery_status STRING DEFAULT 'pending',  -- 'pending', 'sent', 'failed'
  response_received BOOLEAN DEFAULT FALSE,
  response_at TIMESTAMP,
  notes STRING,
  
  PRIMARY KEY (escalation_id) NOT ENFORCED,
  FOREIGN KEY (alert_id) REFERENCES alerts(alert_id) NOT ENFORCED,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id) NOT ENFORCED
);

CREATE INDEX idx_escalations_provider ON care_orchestra.escalations(provider_id, delivery_status);
```

---

### 7. appointments
**Purpose**: Patient appointments

**Schema**:
```sql
CREATE TABLE IF NOT EXISTS care_orchestra.appointments (
  appointment_id STRING NOT NULL,
  patient_id STRING NOT NULL,
  provider_id STRING NOT NULL,
  provider_name STRING,
  appointment_type STRING,  -- 'follow-up', 'routine', 'emergency'
  scheduled_at TIMESTAMP NOT NULL,
  location STRING,
  notes STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  cancelled BOOLEAN DEFAULT FALSE,
  completed BOOLEAN DEFAULT FALSE,
  
  PRIMARY KEY (appointment_id) NOT ENFORCED,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id) NOT ENFORCED
);

CREATE INDEX idx_appointments_patient ON care_orchestra.appointments(patient_id, scheduled_at);
```

---

### 8. followups
**Purpose**: Follow-up reminders

**Schema**:
```sql
CREATE TABLE IF NOT EXISTS care_orchestra.followups (
  followup_id STRING NOT NULL,
  patient_id STRING NOT NULL,
  reason STRING NOT NULL,  -- 'medication_review', 'vitals_check', 'lab_results'
  due_date TIMESTAMP NOT NULL,
  priority STRING DEFAULT 'normal',  -- 'low', 'normal', 'high', 'urgent'
  sent BOOLEAN DEFAULT FALSE,
  responded BOOLEAN DEFAULT FALSE,
  response_date TIMESTAMP,
  notes STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  
  PRIMARY KEY (followup_id) NOT ENFORCED,
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id) NOT ENFORCED
);

CREATE INDEX idx_followups_due_date ON care_orchestra.followups(patient_id, due_date);
```

---

## View Definitions (Useful Queries)

### Active Medications View
```sql
CREATE OR REPLACE VIEW care_orchestra.v_active_medications AS
SELECT 
  patient_id, medication_id, name, dosage, frequency,
  start_date, end_date
FROM care_orchestra.medications
WHERE start_date <= CURRENT_TIMESTAMP()
  AND (end_date IS NULL OR end_date > CURRENT_TIMESTAMP());
```

### Recent Vital Readings View
```sql
CREATE OR REPLACE VIEW care_orchestra.v_recent_vitals AS
SELECT 
  patient_id, vital_type, value, unit, measured_at,
  ROW_NUMBER() OVER (PARTITION BY patient_id, vital_type ORDER BY measured_at DESC) as rn
FROM care_orchestra.vitals
WHERE measured_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
```

### Medication Adherence View
```sql
CREATE OR REPLACE VIEW care_orchestra.v_medication_adherence AS
SELECT 
  patient_id,
  medication_id,
  COUNTIF(taken) / COUNT(*) * 100 as adherence_percentage,
  COUNT(*) as doses_due,
  COUNTIF(NOT taken) as doses_missed
FROM care_orchestra.medication_logs
WHERE scheduled_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY patient_id, medication_id;
```

---

## Data Loading

Use `infra/scripts/load_seed_data.py` to load initial data from CSV files in `data/seed/`.

Schema deployment should be idempotent (use `CREATE TABLE IF NOT EXISTS`).

---

## Performance Considerations

- Partition tables by `patient_id` for large-scale deployment
- Use appropriate expiration for log tables (90 days)
- Create indexes on frequently queried fields
- Use clustering for better query performance

---

## Data Retention Policy (Future)

- Patient records: Retain indefinitely
- Vitals: Retain 2+ years for historical analysis
- Medication logs: Retain 1+ year for adherence tracking
- Alerts: Retain 6+ months for audit trail
- Escalations: Retain indefinitely for compliance
