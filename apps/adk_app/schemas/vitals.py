"""Vitals data schema."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class VitalReading:
    """Single vital sign reading."""
    vital_type: str  # e.g., "blood_pressure", "heart_rate", "glucose"
    value: float
    unit: str  # e.g., "mmHg", "bpm", "mg/dL"
    measured_at: datetime
    
    def __post_init__(self):
        """Validate vital reading."""
        if self.value < 0:
            raise ValueError("Vital value cannot be negative")


@dataclass
class BloodPressure(VitalReading):
    """Blood pressure reading with systolic/diastolic."""
    systolic: int
    diastolic: int
    vital_type: str = "blood_pressure"
    unit: str = "mmHg"


@dataclass
class VitalsRecord:
    """Complete vitals record for a patient."""
    record_id: str
    patient_id: str
    readings: list = field(default_factory=list)  # List of VitalReading objects
    recorded_at: datetime = field(default_factory=datetime.now)
    notes: Optional[str] = None
    
    def add_reading(self, reading: VitalReading) -> None:
        """Add a vital reading to the record."""
        self.readings.append(reading)
    
    def get_latest_by_type(self, vital_type: str) -> Optional[VitalReading]:
        """Get most recent reading of a specific type."""
        matching = [r for r in self.readings if r.vital_type == vital_type]
        return max(matching, key=lambda r: r.measured_at) if matching else None
