"""BigQuery mutations and inserts."""


class PatientMutations:
    """SQL mutations for patient data operations."""
    
    @staticmethod
    def insert_vital(patient_id: str, vital_type: str, value: float, unit: str) -> str:
        """Insert a vital reading."""
        # NOTE: This is a template - actual implementation should use parameterized queries
        return f"""
        INSERT INTO vitals (patient_id, vital_type, value, unit, measured_at)
        VALUES ('{patient_id}', '{vital_type}', {value}, '{unit}', CURRENT_TIMESTAMP())
        """
    
    @staticmethod
    def log_medication_dose(patient_id: str, medication_id: str, taken: bool = True) -> str:
        """Log a medication dose."""
        # NOTE: This is a template - actual implementation should use parameterized queries
        return f"""
        INSERT INTO medication_logs (patient_id, medication_id, scheduled_time, taken, actual_time)
        VALUES ('{patient_id}', '{medication_id}', CURRENT_TIMESTAMP(), {taken}, CURRENT_TIMESTAMP())
        """
    
    @staticmethod
    def create_alert(patient_id: str, alert_type: str, severity: str, title: str, description: str) -> str:
        """Create an alert."""
        # NOTE: This is a template - actual implementation should use parameterized queries
        return f"""
        INSERT INTO alerts (patient_id, alert_type, severity, title, description, created_at)
        VALUES ('{patient_id}', '{alert_type}', '{severity}', '{title}', '{description}', CURRENT_TIMESTAMP())
        """
    
    @staticmethod
    def acknowledge_alert(alert_id: str, acknowledged_by: str = None) -> str:
        """Mark alert as acknowledged."""
        # NOTE: This is a template - actual implementation should use parameterized queries
        if acknowledged_by:
            return f"""
            UPDATE alerts
            SET acknowledged = true, acknowledged_by = '{acknowledged_by}', acknowledged_at = CURRENT_TIMESTAMP()
            WHERE alert_id = '{alert_id}'
            """
        else:
            return f"""
            UPDATE alerts
            SET acknowledged = true, acknowledged_at = CURRENT_TIMESTAMP()
            WHERE alert_id = '{alert_id}'
            """
