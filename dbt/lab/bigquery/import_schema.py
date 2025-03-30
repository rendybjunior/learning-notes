from google.cloud import bigquery
import json
import os

# Set your GCP project and dataset
PROJECT_ID = "PROJECT_ID" # Change this to your project
DATASET_ID = "DATASET_ID" # Change this to your dataset

SCHEMA_FOLDER = f"bq_schemas_sakila"  # Folder where schema JSON files are stored

# Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)

def create_dataset():
    """Creates a dataset in BigQuery if it does not exist."""
    dataset_ref = client.dataset(DATASET_ID)
    
    try:
        client.get_dataset(dataset_ref)  # Check if dataset exists
        print(f"✅ Dataset '{DATASET_ID}' already exists.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"  # Change this if needed
        client.create_dataset(dataset, exists_ok=True)
        print(f"🚀 Created dataset '{DATASET_ID}'.")

def create_table_from_schema(schema_file):
    """Creates a table in BigQuery using a schema JSON file."""
    table_name = os.path.basename(schema_file).replace(".json", "")  # Extract table name
    table_ref = client.dataset(DATASET_ID).table(table_name)

    # Read schema from JSON and correctly map field attributes
    with open(schema_file, "r") as f:
        schema_data = json.load(f)
        schema = [bigquery.SchemaField(field["name"], field["type"], mode=field["mode"]) for field in schema_data]

    table = bigquery.Table(table_ref, schema=schema)

    try:
        client.create_table(table)
        print(f"✅ Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"⚠️ Table '{table_name}' already exists or error occurred: {e}")

def import_all_schemas():
    """Imports all JSON schema files and creates tables."""
    create_dataset()  # Ensure dataset exists

    for filename in os.listdir(SCHEMA_FOLDER):
        if filename.endswith(".json"):
            schema_file = os.path.join(SCHEMA_FOLDER, filename)
            create_table_from_schema(schema_file)

if __name__ == "__main__":
    import_all_schemas()