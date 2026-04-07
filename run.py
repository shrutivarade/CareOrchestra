#!/usr/bin/env python
"""CareOrchestra Application Runner"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.adk_app.app import CareOrchestraApp

if __name__ == "__main__":
    app = CareOrchestraApp()
    print("✅ CareOrchestra initialized successfully!")
    print(f"Agents loaded: {list(app.agents.keys())}")
