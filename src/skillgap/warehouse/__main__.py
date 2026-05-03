"""CLI orchestrator pour le warehouse loader.

Usage:
    uv run --env-file .env python -m skillgap.warehouse

Variables d'env requises:
    GCP_PROJECT_ID      ex: skillgap-493211
    BQ_DATASET_RAW      ex: raw_dev
    BQ_TABLE_OFFERS     ex: offers
    GCS_BUCKET_SILVER   ex: skillgap-silver-dev
    WAREHOUSE_MODE      "incremental" (défaut) ou "backfill"
"""

import os

from skillgap.warehouse.bq_loader import BQLoader


def main() -> None:
    print("skillgap-warehouse v0.1.0")

    project_id = os.environ["GCP_PROJECT_ID"]
    dataset_id = os.environ["BQ_DATASET_RAW"]
    table_id = os.environ.get("BQ_TABLE_OFFERS", "offers")
    silver_bucket = os.environ["GCS_BUCKET_SILVER"]
    mode = os.environ.get("WAREHOUSE_MODE", "incremental").lower()

    print(f"Mode: {mode}")
    print(f"Target: {project_id}.{dataset_id}.{table_id}")
    print(f"Source: gs://{silver_bucket}/france_travail/")

    loader = BQLoader(
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
        silver_bucket=silver_bucket,
    )

    if mode == "incremental":
        rows = loader.load_incremental()
    elif mode == "backfill":
        rows = loader.load_backfill()
    else:
        raise ValueError(f"Unknown WAREHOUSE_MODE: {mode}. Expected 'incremental' or 'backfill'.")

    print(f"Total rows loaded: {rows}")


if __name__ == "__main__":
    main()
