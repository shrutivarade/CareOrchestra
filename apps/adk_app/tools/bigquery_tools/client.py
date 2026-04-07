"""BigQuery client and utilities."""

import logging
from typing import Optional, List, Dict, Any
from google.cloud import bigquery
from google.cloud.bigquery import QueryJob

logger = logging.getLogger(__name__)


class BigQueryClient:
    """Client for BigQuery data operations."""
    
    def __init__(self, project_id: str, dataset_id: str):
        """
        Initialize BigQuery client.
        
        Args:
            project_id: GCP project ID
            dataset_id: BigQuery dataset ID
        """
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=project_id)
        logger.info(f"BigQueryClient initialized for project: {project_id}, dataset: {dataset_id}")
    
    async def query(self, sql: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """
        Execute a SQL query.
        
        Args:
            sql: SQL query string
            parameters: Query parameters (optional)
            
        Returns:
            Query results as list of dictionaries
        """
        try:
            # Configure query job
            job_config = bigquery.QueryJobConfig()
            if parameters:
                job_config.query_parameters = [
                    bigquery.ScalarQueryParameter(key, "STRING", value)
                    for key, value in parameters.items()
                ]
            
            # Execute query
            logger.debug(f"Executing query: {sql}")
            query_job: QueryJob = self.client.query(sql, job_config=job_config)
            results = query_job.result()
            
            # Convert results to list of dictionaries
            rows = [dict(row) for row in results]
            logger.info(f"Query returned {len(rows)} rows")
            return rows
            
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise
    
    async def insert(self, table: str, rows: List[Dict]) -> bool:
        """
        Insert rows into a table.
        
        Args:
            table: Table name (e.g., 'patients', 'vitals')
            rows: List of row dictionaries
            
        Returns:
            Success status
        """
        if not rows:
            logger.warning("No rows to insert")
            return False
        
        try:
            table_id = f"{self.project_id}.{self.dataset_id}.{table}"
            logger.info(f"Inserting {len(rows)} rows into {table_id}")
            
            errors = self.client.insert_rows_json(table_id, rows)
            
            if errors:
                logger.error(f"Insert errors: {errors}")
                return False
            
            logger.info(f"Successfully inserted {len(rows)} rows")
            return True
            
        except Exception as e:
            logger.error(f"Insert failed: {str(e)}")
            raise
    
    async def update(self, table: str, where_clause: str, updates: Dict) -> int:
        """
        Update rows in a table.
        
        Args:
            table: Table name
            where_clause: WHERE clause for update (e.g., "patient_id = @patient_id")
            updates: Dictionary of fields to update
            
        Returns:
            Number of rows updated
        """
        try:
            # Build SET clause
            set_clause = ", ".join([f"{key} = @{key}" for key in updates.keys()])
            
            # Build full UPDATE query
            sql = f"""
                UPDATE `{self.project_id}.{self.dataset_id}.{table}`
                SET {set_clause}
                WHERE {where_clause}
            """
            
            logger.info(f"Executing update on {table}: {sql}")
            
            # Merge updates with where parameters for query job
            job_config = bigquery.QueryJobConfig()
            all_params = {**updates}
            
            # Parse where_clause to extract parameter names
            # This is a simplified approach - in production, use proper parameter handling
            query_job: QueryJob = self.client.query(sql, job_config=job_config)
            result = query_job.result()
            
            affected_rows = query_job.total_bytes_processed or 0
            logger.info(f"Update complete")
            return affected_rows
            
        except Exception as e:
            logger.error(f"Update failed: {str(e)}")
            raise
