# BigQuery Sakila Dataset

## Prerequisites

Run `pip install -r requirements.txt` and authorized yourself to GCP e.g. using `gcloud auth`.

## Import Sakila Dataset to BQ

1. Run `import_schema.py`
2. Either
  - Run `import_data.py`, or
  - Run the sql script inside `bq_insert_sakila` (note: it will take sometime).