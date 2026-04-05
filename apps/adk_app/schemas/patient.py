"""Patient data schema."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Patient:
    """Patient information schema."""
    patient_id: str
    first_name: str
    last_name: str
    date_of_birth: str
    phone_number: str
    email: str
    conditions: List[str] = field(default_factory=list)  # e.g., ["hypertension", "diabetes"]
    care_team: List[str] = field(default_factory=list)  # Doctor IDs
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    @property
    def full_name(self) -> str:
        """Get full patient name."""
        return f"{self.first_name} {self.last_name}"
