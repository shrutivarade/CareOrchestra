"""Pytest configuration for CareOrchestra tests."""

import asyncio
import pytest
from pathlib import Path
import sys

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_patient_data():
    """Provide mock patient data for tests."""
    return {
        "patient_id": "PT_TEST_001",
        "first_name": "Test",
        "last_name": "Patient",
        "date_of_birth": "1960-01-01",
        "phone_number": "(555) 555-5555",
        "email": "test@example.com",
        "conditions": ["hypertension", "diabetes"],
        "care_team": ["DR_TEST_001"]
    }


@pytest.fixture
def mock_vitals_data():
    """Provide mock vitals data for tests."""
    return {
        "patient_id": "PT_TEST_001",
        "vital_type": "blood_pressure",
        "systolic": 150,
        "diastolic": 95,
        "unit": "mmHg",
        "measured_at": "2025-04-05T10:00:00Z"
    }


@pytest.fixture
def mock_alert_data():
    """Provide mock alert data for tests."""
    return {
        "alert_id": "ALT_TEST_001",
        "patient_id": "PT_TEST_001",
        "alert_type": "vital_abnormal",
        "severity": "high",
        "title": "Test Alert",
        "description": "This is a test alert"
    }


@pytest.fixture
def mock_medication_data():
    """Provide mock medication data for tests."""
    return {
        "medication_id": "MED_TEST_001",
        "patient_id": "PT_TEST_001",
        "name": "Test Medication",
        "dosage": "10mg",
        "frequency": "once daily",
        "reason": "test"
    }
