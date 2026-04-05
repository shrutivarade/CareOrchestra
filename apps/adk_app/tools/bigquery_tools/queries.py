"""BigQuery queries for patient data."""


class PatientQueries:
    """SQL queries for patient data."""
    
    @staticmethod
    def get_patient(patient_id: str) -> str:
        """Get patient by ID."""
        return f"""
        SELECT * FROM patients
        WHERE patient_id = '{patient_id}'
        """
    
    @staticmethod
    def get_recent_vitals(patient_id: str, days: int = 30) -> str:
        """Get recent vitals for patient."""
        return f"""
        SELECT * FROM vitals
        WHERE patient_id = '{patient_id}'
          AND measured_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        ORDER BY measured_at DESC
        """
    
    @staticmethod
    def get_active_medications(patient_id: str) -> str:
        """Get active medications for patient."""
        return f"""
        SELECT * FROM medications
        WHERE patient_id = '{patient_id}'
          AND start_date <= CURRENT_TIMESTAMP()
          AND (end_date IS NULL OR end_date > CURRENT_TIMESTAMP())
        """
    
    @staticmethod
    def get_medication_logs(patient_id: str, days: int = 7) -> str:
        """Get medication logs for adherence tracking."""
        return f"""
        SELECT * FROM medication_logs
        WHERE patient_id = '{patient_id}'
          AND scheduled_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        ORDER BY scheduled_time DESC
        """
    
    @staticmethod
    def get_recent_alerts(patient_id: str, days: int = 7) -> str:
        """Get recent alerts for patient."""
        return f"""
        SELECT * FROM alerts
        WHERE patient_id = '{patient_id}'
          AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY)
        ORDER BY created_at DESC
        """
