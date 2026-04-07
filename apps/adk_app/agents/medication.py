import os
import json
import logging
import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import google.cloud.logging
from dotenv import load_dotenv
from ..tools import get_mcp_manager

# --- Setup Logging and Environment ---
try:
    cloud_logging_client = google.cloud.logging.Client()
    cloud_logging_client.setup_logging()
except Exception:
    logging.basicConfig(level=logging.INFO)
    logging.info("Cloud logging not available, using standard logging.")

load_dotenv()
logger = logging.getLogger(__name__)


async def fetch_patient_medications(patient_id: str) -> list:
    """
    Fetch medications for a patient from BigQuery via MCP.
    
    Args:
        patient_id: The patient ID
        
    Returns:
        List of medication records
    """
    try:
        mcp_manager = get_mcp_manager()
        medications = await mcp_manager.execute_tool("get_medications")
        
        # Filter for the specific patient
        patient_meds = [m for m in medications if m.get("patient_id") == patient_id]
        
        logger.info(f"Fetched {len(patient_meds)} medications for patient {patient_id}")
        return patient_meds
    except Exception as e:
        logger.error(f"Failed to fetch medications: {e}")
        return []


def save_medication_response(
    patient_id: str,
    patient_name: str,
    medication: str,
    medication_taken: bool,
    raw_response: str,
) -> dict:
    """
    Builds and saves a structured medication check-in record.
    Call this after the patient confirms whether they took their medication.
    
    Args:
        patient_id: The ID of the patient.
        patient_name: The name of the patient.
        medication: The medication name being tracked.
        medication_taken: True if patient confirmed taking medication.
        raw_response: The patient's verbatim reply text.
    """
    now = datetime.datetime.utcnow()

    medication_record = {
        "patient_id":          patient_id,
        "patient_name":        patient_name,
        "medication":          medication,
        "date":                now.strftime("%Y-%m-%d"),
        "time":                now.strftime("%H:%M:%S"),
        "timezone":            "UTC",
        "medication_response": "yes" if medication_taken else "no",
        "raw_response":        raw_response,
        "reminder_sent":       True,
        "follow_up_message": (
            "Great job! Keep it up."
            if medication_taken
            else "Please take your medicines on time tomorrow."
        ),
    }

    # In a real app, this would be an INSERT INTO BigQuery or Postgres
    logger.info(f"[Medication Record Saved] {json.dumps(medication_record)}")

    return {
        "status":            "success",
        "medication_record": medication_record,
    }


class MedicationAgent:
    """
    Main class-based wrapper for the Medication Agent logic.
    Integrates with MCP tools to fetch and track medication adherence.
    """
    def __init__(self):
        self.agent_name = "MedicationAgent"
        self.mcp_manager = get_mcp_manager()

    async def check_medication_adherence(self, patient_id: str) -> dict:
        """
        Check medication adherence for a patient.
        
        Args:
            patient_id: Patient ID to check
            
        Returns:
            Adherence status and medication list
        """
        try:
            medications = await fetch_patient_medications(patient_id)
            
            if not medications:
                return {
                    "status": "no_data",
                    "patient_id": patient_id,
                    "message": "No medication data found"
                }
            
            # Analyze adherence pattern
            total = len(medications)
            adherent = len([m for m in medications if m.get("adherence_status") == "adherent"])
            adherence_rate = (adherent / total * 100) if total > 0 else 0
            
            status = "good" if adherence_rate >= 80 else "needs_improvement"
            
            return {
                "status": status,
                "patient_id": patient_id,
                "medications": medications,
                "adherence_rate": adherence_rate,
                "total_medications": total,
                "adherent_count": adherent
            }
        except Exception as e:
            logger.error(f"Failed to check medication adherence: {e}")
            return {
                "status": "error",
                "patient_id": patient_id,
                "message": str(e)
            }

    async def get_patient_medications(self, patient_id: str) -> list:
        """
        Get list of medications for a patient.
        
        Args:
            patient_id: Patient ID
            
        Returns:
            List of medication dictionaries
        """
        return await fetch_patient_medications(patient_id)