from google.cloud import bigquery

from bigquery.dataset import ensure_dataset_exists
from bigquery.datatable import ensure_table_exists

def setup_build_table(
    client: bigquery.Client,
    dataset_id: str,
    table_id: str = "builds",
    location: str = "US"
) -> None:
    """
    Sets up the BigQuery dataset and table for storing builds if they don't exist.
    
    Args:
        client: BigQuery client
        dataset_id: ID of the dataset to store builds
        table_id: ID of the table to store builds
        location: Geographic location of the dataset
    """
    try:
        # Ensure dataset exists
        dataset: bigquery.Dataset = ensure_dataset_exists(client, dataset_id, location)
        
        # Define schema for builds table
        schema = [
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("closed_at", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("commit", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("branch", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("repo", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("last_updated_date", "TIMESTAMP", mode="REQUIRED")
        ]
        
        # Ensure table exists with proper schema
        ensure_table_exists(
            client=client,
            dataset_id=dataset_id,
            table_id=table_id,
            schema=schema,
            partition_by="created_at",
            clustering_fields=["repo", "branch"],
            partition_type=bigquery.TimePartitioningType.MONTH
        )
    except Exception as e:
        raise RuntimeError(f"Failed to setup build table: {table_id} in dataset: {dataset_id}") from e