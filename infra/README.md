# Infrastructure & Deployment Scripts

This folder contains scripts for infrastructure setup and deployment.

## Scripts

### setup.sh
Sets up development environment:
- Creates Python virtual environment
- Installs dependencies from requirements.txt
- Creates .env from .env.example
- Initializes BigQuery schema

**Usage**:
```bash
bash infra/scripts/setup.sh
```

### load_seed_data.py
Loads mock patient data into BigQuery:
- Creates BigQuery dataset and tables
- Loads patients, vitals, medications, and adherence data from data/seed/*.csv
- Sets up sample appointments and alerts

**Usage**:
```bash
python infra/scripts/load_seed_data.py
```

### deploy.sh
Deploys CareOrchestra to Google Cloud Run:
- Builds Docker image
- Pushes to Google Container Registry
- Deploys to Cloud Run with environment variables

**Usage**:
```bash
bash infra/scripts/deploy.sh --project-id YOUR_PROJECT_ID
```

## Implementation Notes

These are placeholder scripts. Full implementation will include:

- Database schema creation
- Data loading with proper validation
- Docker containerization
- Google Cloud integration
- Environment validation
- Error handling and logging

See main [documentation](../../docs/) for deployment architecture.
