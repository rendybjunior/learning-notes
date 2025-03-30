from google.cloud import bigquery
import json
import os

# Set your GCP project and dataset
PROJECT_ID = "PROJECT_ID"
DATASET_ID = "sakila"

# Set the output folder
OUTPUT_FOLDER = f"bq_schemas_{DATASET_ID}"

# Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)

# Ensure the output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def export_schema(table_id):
    """Exports BigQuery table schema, removes 'sakila_' prefix, and excludes 'datastream_metadata' column."""
    table_ref = client.dataset(DATASET_ID).table(table_id)
    table = client.get_table(table_ref)

    # Remove 'sakila_' prefix if it exists
    clean_table_name = table_id.replace("sakila_", "")

    # Exclude 'datastream_metadata' column
    schema = [
        {"name": field.name, "type": field.field_type, "mode": field.mode}
        for field in table.schema if field.name.lower() != "datastream_metadata"
    ]

    output_path = os.path.join(OUTPUT_FOLDER, f"{clean_table_name}.json")
    with open(output_path, "w") as f:
        json.dump(schema, f, indent=4)

    print(f"✅ Schema exported (without 'datastream_metadata'): {output_path}")

def export_all_schemas():
    """Exports schemas for all tables in the specified dataset."""
    tables = client.list_tables(DATASET_ID)
    for table in tables:
        export_schema(table.table_id)

if __name__ == "__main__":
    export_all_schemas()