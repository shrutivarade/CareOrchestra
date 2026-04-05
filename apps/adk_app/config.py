"""Configuration management for CareOrchestra ADK application."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class GoogleConfig:
    """Google Cloud configuration."""
    project_id: str = os.getenv("GCP_PROJECT_ID", "")
    location: str = os.getenv("GCP_LOCATION", "us-central1")
    bigquery_dataset: str = os.getenv("BIGQUERY_DATASET", "care_orchestra")


@dataclass
class GmailConfig:
    """Gmail integration configuration."""
    sender_email: str = os.getenv("GMAIL_SENDER_EMAIL", "")
    use_mock: bool = os.getenv("GMAIL_USE_MOCK", "true").lower() == "true"


@dataclass
class CalendarConfig:
    """Google Calendar integration configuration."""
    calendar_id: str = os.getenv("CALENDAR_ID", "primary")
    use_mock: bool = os.getenv("CALENDAR_USE_MOCK", "true").lower() == "true"


@dataclass
class AppConfig:
    """Main application configuration."""
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Agent configuration
    use_mock_data: bool = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
    mock_data_path: str = os.getenv("MOCK_DATA_PATH", "data/mock_payloads")
    
    # Service configuration
    google: GoogleConfig = GoogleConfig()
    gmail: GmailConfig = GmailConfig()
    calendar: CalendarConfig = CalendarConfig()


def get_config() -> AppConfig:
    """Get application configuration."""
    return AppConfig()
