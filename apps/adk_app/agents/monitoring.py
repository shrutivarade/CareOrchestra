"""Monitoring Agent - Watches for patient events and triggers analysis."""

import logging
import asyncio
from ..tools import get_mcp_manager

logger = logging.getLogger(__name__)


class MonitoringAgent:
    """
    Collects, validates, and routes the summarized data from the Coordinator.
    Integrates with MCP tools to fetch open alerts and patient context.
    """
    
    def __init__(self):
        """Initialize the monitoring agent."""
        self.mcp_manager = get_mcp_manager()
    
    async def _fetch_open_alerts(self, patient_id: str = None):
        """
        Fetch open alerts from BigQuery via MCP.
        
        Args:
            patient_id: Optional patient ID to filter alerts (future enhancement)
            
        Returns:
            List of open alert dictionaries
        """
        try:
            alerts = await self.mcp_manager.execute_tool("get_open_alerts")
            
            # Filter for specific patient if provided
            if patient_id:
                alerts = [a for a in alerts if a.get("patient_id") == patient_id]
            
            logger.info(f"Fetched {len(alerts)} open alerts")
            return alerts
        except Exception as e:
            logger.error(f"Failed to fetch alerts: {e}")
            return []
    
    def process_summary(self, patient_id: str, summary: str):
        """
        Process patient summary and determine appropriate action.
        
        Args:
            patient_id: The patient ID
            summary: Clinical summary from coordinator
            
        Returns:
            Clinical recommendation or escalation message
        """
        # 1. Check for critical keywords (emergency signals)
        critical_keywords = ["chest pain", "can't breathe", "difficulty breathing", "unconscious", "severe"]
        if any(keyword in summary.lower() for keyword in critical_keywords):
            return "🚨 URGENT: Escalating to emergency nursing team immediately."
        
        # 2. Check for high-risk indicators
        if "high bp" in summary.lower() or "hypertension" in summary.lower():
            return "⚠️ HIGH RISK: Abnormal vitals detected. Recommending urgent doctor contact within 2 hours."
        
        if "medication" in summary.lower() and "missed" in summary.lower():
            return "⚠️ Medication adherence issue detected. Sending reminder and scheduling follow-up call."
        
        # 3. Default: Stable status
        return "✓ Everything looks stable based on your report. I've logged this for your doctor to review."