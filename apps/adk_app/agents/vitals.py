"""Vitals Agent - Analyzes vital signs and detects abnormal patterns."""

import logging
from ..tools import get_mcp_manager

logger = logging.getLogger(__name__)


class VitalsAgent:
    """
    Analyzes vital signs:
    - Reads vital history (BP, heart rate, glucose, oxygen, etc.)
    - Detects abnormal values
    - Identifies trends (improving, worsening, stable)
    - Flags concerning patterns for escalation
    """

    def __init__(self):
        """Initialize vitals agent."""
        self.mcp_manager = get_mcp_manager()

    # -------------------------------
    # INTERNAL: Fetch vitals from BigQuery via MCP
    # -------------------------------
    async def _fetch_vitals(self, patient_id: str):
        """
        Fetch patient vital signs from BigQuery using MCP tools.
        
        Args:
            patient_id: Patient ID to fetch vitals for
            
        Returns:
            List of vital sign dictionaries
        """
        try:
            vitals = await self.mcp_manager.execute_tool("get_recent_vitals")
            
            # Filter for the specific patient
            patient_vitals = [v for v in vitals if v.get("patient_id") == patient_id]
            
            if patient_vitals:
                logger.info(f"Fetched {len(patient_vitals)} vital records for patient {patient_id}")
                return patient_vitals
            else:
                logger.warning(f"No vital data found for patient {patient_id}")
                # Return empty list instead of mock data
                return []
                
        except Exception as e:
            logger.error(f"Failed to fetch vitals: {e}")
            return []

    # -------------------------------
    # RULES (can later move to risk_rules/vitals_rules.py)
    # -------------------------------
    def _apply_rules(self, vitals):
        """Apply clinical rules to detect abnormal values."""
        issues = []
        
        if not vitals:
            return issues
        
        latest = vitals[0]

        # Blood Pressure
        systolic = latest.get("bp_systolic") or latest.get("value")
        if systolic and systolic > 140:
            issues.append({"type": "blood_pressure", "level": "high", "value": systolic})

        # Glucose
        glucose = latest.get("glucose")
        if glucose and glucose > 140:
            issues.append({"type": "glucose", "level": "high", "value": glucose})

        # Oxygen Saturation
        spo2 = latest.get("spo2")
        if spo2 and spo2 < 95:
            issues.append({"type": "spo2", "level": "low", "value": spo2})

        # Heart Rate
        hr = latest.get("heart_rate")
        if hr and hr > 100:
            issues.append({"type": "heart_rate", "level": "high", "value": hr})

        return issues

    # -------------------------------
    # ANOMALY DETECTION
    # -------------------------------
    def _detect_anomalies(self, vitals):
        """Detect sudden changes in vital signs."""
        anomalies = []

        if len(vitals) < 2:
            return anomalies

        latest = vitals[0]
        prev = vitals[1]

        # Check for sudden glucose change
        latest_glucose = latest.get("value") if latest.get("vital_type") == "glucose" else latest.get("glucose")
        prev_glucose = prev.get("value") if prev.get("vital_type") == "glucose" else prev.get("glucose")
        
        if latest_glucose and prev_glucose and abs(latest_glucose - prev_glucose) > 20:
            anomalies.append("sudden glucose change")

        # Check for abnormal flag from database
        if latest.get("abnormal_flag"):
            anomalies.append(f"abnormal {latest.get('vital_type', 'vital')}")

        return anomalies

    # -------------------------------
    # TREND CALCULATION
    # -------------------------------
    def _calculate_trend(self, values):
        """Calculate trend (increasing, decreasing, stable) from values."""
        if len(values) < 2:
            return "insufficient_data"

        if values[-1] > values[0] * 1.1:  # More than 10% increase
            return "increasing"
        elif values[-1] < values[0] * 0.9:  # More than 10% decrease
            return "decreasing"
        return "stable"

    async def analyze_vitals(self, patient_id: str) -> dict:
        """
        Analyze patient vitals from BigQuery.
        
        Args:
            patient_id: Patient ID to analyze
            
        Returns:
            Analysis result with status, issues, anomalies, and trends
        """
        # ✅ 1. Query recent vitals from BigQuery
        vitals = await self._fetch_vitals(patient_id)

        if not vitals:
            return {
                "status": "no_data",
                "patient_id": patient_id,
                "message": "No recent vital data available"
            }

        latest = vitals[0]

        # ✅ 2. Apply rules
        issues = self._apply_rules(vitals)

        # ✅ 3. Detect anomalies
        anomalies = self._detect_anomalies(vitals)

        # ✅ 4. Identify trends (simplified)
        trends = {
            "overall": "stable" if not issues else "warning"
        }

        # ✅ 5. Final result
        status = "normal"
        if issues or anomalies:
            status = "alert"

        return {
            "status": status,
            "patient_id": patient_id,
            "latest_vitals": latest,
            "issues": issues,
            "anomalies": anomalies,
            "trends": trends,
            "total_records": len(vitals)
        }

    async def check_trend(self, patient_id: str, vital_type: str) -> dict:
        """
        Check trend for specific vital over time.
        
        Args:
            patient_id: Patient ID
            vital_type: Type of vital to check (e.g., 'glucose', 'blood_pressure')
            
        Returns:
            Trend analysis with risk assessment
        """
        # ✅ 1. Query historical vitals
        vitals = await self._fetch_vitals(patient_id)

        if not vitals:
            return {
                "vital_type": vital_type,
                "trend": "insufficient_data",
                "risk": "unknown",
                "message": "No vital data available"
            }

        # Extract values for the specific vital type
        values = []
        for v in reversed(vitals):
            # Try different field names
            if v.get("vital_type") == vital_type:
                val = v.get("value")
                if val:
                    values.append(val)
            elif vital_type in v:
                values.append(v[vital_type])

        if not values:
            return {
                "vital_type": vital_type,
                "trend": "no_data",
                "risk": "unknown",
                "message": f"No {vital_type} data found"
            }

        # ✅ 2. Compute trend
        trend = self._calculate_trend(values)

        # ✅ 3. Assess risk
        risk = "normal"
        if trend == "increasing":
            risk = "warning"
        elif trend == "decreasing":
            risk = "improving"

        return {
            "vital_type": vital_type,
            "trend": trend,
            "risk": risk,
            "data_points": len(values)
        }