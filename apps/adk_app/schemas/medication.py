"""Medication data schema."""

from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Optional, List


@dataclass
class Medication:
    """Medication information."""
    medication_id: str
    patient_id: str
    name: str
    dosage: str  # e.g., "500mg"
    frequency: str  # e.g., "twice daily", "once daily"
    start_date: datetime
    end_date: Optional[datetime] = None
    reason: Optional[str] = None  # e.g., "hypertension", "diabetes"
    notes: Optional[str] = None
    

@dataclass
class MedicationSchedule:
    """Medication schedule for a patient."""
    patient_id: str
    medications: List[Medication] = field(default_factory=list)
    schedule_times: dict = field(default_factory=dict)  # Times when meds should be taken
    
    def add_medication(self, medication: Medication) -> None:
        """Add medication to schedule."""
        self.medications.append(medication)
    
    def get_active_medications(self) -> List[Medication]:
        """Get current active medications."""
        now = datetime.now()
        return [
            m for m in self.medications
            if m.start_date <= now and (m.end_date is None or m.end_date > now)
        ]


@dataclass
class MedicationLog:
    """Log of medication adherence."""
    log_id: str
    patient_id: str
    medication_id: str
    scheduled_time: datetime
    actual_time: Optional[datetime] = None
    taken: bool = False
    notes: Optional[str] = None
    
    def mark_taken(self, actual_time: datetime = None) -> None:
        """Mark medication as taken."""
        self.taken = True
        self.actual_time = actual_time or datetime.now()
    
    def is_missed(self, grace_period_minutes: int = 60) -> bool:
        """Check if dose was missed (not taken within grace period)."""
        if self.taken:
            return False
        now = datetime.now()
        time_diff = (now - self.scheduled_time).total_seconds() / 60
        return time_diff > grace_period_minutes
