import os
import json
from google.cloud import bigquery

# Set your GCP project and dataset
PROJECT_ID = "PROJECT_ID"
DEFAULT_DATASET_ID = "sakila" # DO NOT change this
TARGET_DATASET_ID = None #"sakila2"  # Change this if needed
JSON_FOLDER = "bq_exports_sakila"  # Folder containing JSON files

# Initialize BigQuery client
client = bigquery.Client(project=PROJECT_ID)

def replace_dataset_name(table_id):
    """Replace dataset name in table references if needed."""
    if TARGET_DATASET_ID and TARGET_DATASET_ID != DEFAULT_DATASET_ID:
        return table_id.replace(f"{DEFAULT_DATASET_ID}.", f"{TARGET_DATASET_ID}.")
    return table_id

def insert_json_data(table_id, json_data):
    """Insert JSON data into an existing BigQuery table."""
    table_ref = f"{PROJECT_ID}.{table_id}"
    table_ref = replace_dataset_name(table_ref)

    errors = client.insert_rows_json(table_ref, json_data)
    if errors:
        print(f"❌ Errors inserting into {table_ref}: {errors}")
    else:
        print(f"✅ Inserted {len(json_data)} rows into {table_ref}")

def import_json_files():
    """Import all JSON files from the folder into BigQuery."""
    if not os.path.exists(JSON_FOLDER):
        print(f"⚠️ Folder '{JSON_FOLDER}' does not exist.")
        return

    json_files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json")]

    if not json_files:
        print("⚠️ No JSON files found.")
        return

    for json_file in json_files:
        table_id = json_file.replace(".json", "")  # Remove .json to get table name
        table_id = f"{DEFAULT_DATASET_ID}.{table_id}"

        print(f"🚀 Processing {json_file}...")

        with open(os.path.join(JSON_FOLDER, json_file), "r", encoding="utf-8") as f:
            json_data = json.load(f)

        if not json_data:
            print(f"⚠️ Skipping empty file: {json_file}")
            continue

        insert_json_data(table_id, json_data)

if __name__ == "__main__":
    import_json_files()
