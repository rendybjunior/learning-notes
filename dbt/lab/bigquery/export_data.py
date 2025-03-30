import os
import json
from decimal import Decimal
from google.cloud import bigquery
import datetime

# Set your GCP project and dataset
PROJECT_ID = "PROJECT_ID"
DATASET_ID = "sakila"
OUTPUT_FOLDER = f"bq_exports_{DATASET_ID}"
TABLE_PREFIX_TO_REMOVE = "" # "sakila_"  # Remove this prefix from table names
EXCLUDED_COLUMNS = {} #{"datastream_metadata"}  # Columns to exclude

# Initialize BigQuery client
bq_client = bigquery.Client(project=PROJECT_ID)

def get_table_list():
    """Fetch all tables in the dataset."""
    tables = bq_client.list_tables(f"{PROJECT_ID}.{DATASET_ID}")
    return [table.table_id for table in tables]

def serialize_json(obj):
    """Convert non-serializable objects (datetime, Decimal) to JSON-friendly formats."""
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()  # 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS'
    elif isinstance(obj, Decimal):
        return float(obj)  # Convert NUMERIC/BIGNUMERIC to float
    return obj

def export_table_to_json(table_id):
    """Query a BigQuery table, exclude columns, and save it as a JSON file."""
    clean_table_name = table_id.replace(TABLE_PREFIX_TO_REMOVE, "")
    output_file = os.path.join(OUTPUT_FOLDER, f"{clean_table_name}.json")

    # Fetch schema to exclude unwanted columns
    table = bq_client.get_table(f"{PROJECT_ID}.{DATASET_ID}.{table_id}")
    included_columns = [field.name for field in table.schema if field.name not in EXCLUDED_COLUMNS]

    if not included_columns:
        print(f"⚠️ Skipping table '{table_id}' because no valid columns remain after filtering.")
        return

    query = f"""
    SELECT {', '.join(included_columns)}
    FROM `{PROJECT_ID}.{DATASET_ID}.{table_id}`
    """

    # Run query and fetch results
    query_job = bq_client.query(query)
    rows = query_job.result()

     # Convert rows to JSON format with datetime handling
    json_data = [ {col: serialize_json(row[col]) for col in included_columns} for row in rows ]


    # Save JSON to a file
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Exported {table_id} to {output_file}")

def export_all_tables():
    """Export all tables in a dataset to JSON files locally."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    tables = get_table_list()
    if not tables:
        print("⚠️ No tables found in dataset.")
        return

    for table in tables:
        export_table_to_json(table)

if __name__ == "__main__":
    export_all_tables()