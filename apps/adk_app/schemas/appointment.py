"""Appointment and scheduling schema."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Appointment:
    """Patient appointment record."""
    appointment_id: str
    patient_id: str
    provider_id: str
    provider_name: str
    appointment_type: str  # e.g., "follow-up", "routine", "emergency"
    scheduled_at: datetime
    location: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    cancelled: bool = False
    completed: bool = False


@dataclass
class FollowUp:
    """Follow-up reminder for patient."""
    followup_id: str
    patient_id: str
    reason: str  # e.g., "medication review", "vitals check", "lab results"
    due_date: datetime
    priority: str = "normal"  # low, normal, high, urgent
    sent: bool = False
    responded: bool = False
    response_date: Optional[datetime] = None
    notes: Optional[str] = None
    
    def is_overdue(self) -> bool:
        """Check if follow-up is overdue."""
        return datetime.now() > self.due_date
    
    def days_until_due(self) -> int:
        """Days until follow-up is due."""
        delta = self.due_date - datetime.now()
        return delta.days
