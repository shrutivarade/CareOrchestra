"""Alert and escalation schema."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class AlertLevel(str, Enum):
    """Alert severity levels."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class AlertType(str, Enum):
    """Types of alerts."""
    VITAL_ABNORMAL = "vital_abnormal"
    MEDICATION_MISSED = "medication_missed"
    APPOINTMENT_DUE = "appointment_due"
    TREND_WARNING = "trend_warning"
    CRITICAL_EVENT = "critical_event"


@dataclass
class Alert:
    """Patient alert."""
    alert_id: str
    patient_id: str
    alert_type: AlertType
    severity: AlertLevel
    title: str
    description: str
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


@dataclass
class Escalation:
    """Escalation to healthcare provider."""
    escalation_id: str
    alert_id: str
    patient_id: str
    provider_id: str
    provider_email: str
    alert_content: str
    sent_at: datetime = field(default_factory=datetime.now)
    delivery_status: str = "pending"  # pending, sent, failed
    response_received: bool = False
    response_at: Optional[datetime] = None
    notes: Optional[str] = None


@dataclass
class AlertHistory:
    """Historical record of patient alerts."""
    patient_id: str
    alerts: List[Alert] = field(default_factory=list)
    
    def add_alert(self, alert: Alert) -> None:
        """Add alert to history."""
        self.alerts.append(alert)
    
    def get_recent_alerts(self, days: int = 7) -> List[Alert]:
        """Get alerts from recent period."""
        cutoff = datetime.now()
        return [
            a for a in self.alerts
            if (datetime.now() - a.created_at).days <= days
        ]
