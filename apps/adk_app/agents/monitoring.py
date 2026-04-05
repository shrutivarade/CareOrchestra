"""Monitoring Agent - Watches for patient events and triggers analysis."""


class MonitoringAgent:
    """
    Monitors patient-related events:
    - Scheduled vitals checks
    - Medication reminders
    - Appointment follow-ups
    - User input events
    - Triggers downstream analysis when events occur
    """
    
    def __init__(self):
        """Initialize monitoring agent."""
        pass
    
    async def monitor(self) -> None:
        """
        Monitor for incoming patient events.
        
        Watches for:
        - Scheduled events from scheduler
        - Manual vitals entry
        - Medication log events
        - Appointment reminders
        """
        # TODO: Implement event monitoring loop
        # TODO: Check for triggered events
        # TODO: Route to coordinator agent
        pass
    
    async def process_event(self, event: dict) -> None:
        """
        Process a detected event.
        
        Args:
            event: Patient event data
        """
        # TODO: Validate event
        # TODO: Enrich with patient context
        # TODO: Pass to coordinator
        pass
