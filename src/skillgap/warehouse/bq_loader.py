"""Loader silver Parquet (GCS) -> BigQuery raw_${env}.offers.

Idempotent par partition: à chaque run, charge la (ou les) partition(s)
silver vers BQ en mode WRITE_TRUNCATE sur la partition correspondante.
"""

from __future__ import annotations

import re
from datetime import date

from google.cloud import bigquery
from google.cloud.storage import Client as StorageClient  # type: ignore[import-untyped]

# Layout silver: gs://<bucket>/france_travail/date=YYYY-MM-DD/*.parquet
SILVER_PREFIX = "france_travail/"
DATE_FOLDER_RE = re.compile(r"^france_travail/date=(\d{4}-\d{2}-\d{2})/$")


class BQLoader:
    """Charge les fichiers Parquet silver dans BigQuery."""

    def __init__(
        self,
        project_id: str,
        dataset_id: str,
        table_id: str,
        silver_bucket: str,
    ) -> None:
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.silver_bucket = silver_bucket
        self.bq_client = bigquery.Client(project=project_id)
        self.gcs_client = StorageClient(project=project_id)

    def list_silver_partitions(self) -> list[date]:
        """Liste les partitions silver disponibles, triées par date croissante."""
        bucket = self.gcs_client.bucket(self.silver_bucket)
        # delimiter='/' pour ne récupérer que les "dossiers" de premier niveau
        # sous le préfixe france_travail/date=
        iterator = self.gcs_client.list_blobs(bucket, prefix=SILVER_PREFIX, delimiter="/")
        # Force la consommation pour peupler `prefixes`
        list(iterator)
        partitions: list[date] = []
        for prefix in sorted(iterator.prefixes):
            match = DATE_FOLDER_RE.match(prefix)
            if match:
                partitions.append(date.fromisoformat(match.group(1)))
        return sorted(partitions)

    def load_partition(self, scrape_date: date) -> int:
        """Charge une partition silver dans BQ (WRITE_TRUNCATE sur cette partition).

        Retourne le nombre de lignes chargées.
        """
        partition_str = scrape_date.strftime("%Y%m%d")
        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}${partition_str}"
        source_uri = (
            f"gs://{self.silver_bucket}/france_travail/date={scrape_date.isoformat()}/*.parquet"
        )

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            parquet_options=bigquery.ParquetOptions.from_api_repr({"enableListInference": True}),
        )

        print(f"[bq_loader] Loading {source_uri} -> {table_ref}")
        load_job = self.bq_client.load_table_from_uri(source_uri, table_ref, job_config=job_config)
        load_job.result()  # bloque jusqu'à completion, lève en cas d'erreur

        rows = load_job.output_rows or 0
        print(f"[bq_loader] Loaded {rows} rows for partition {scrape_date}")
        return rows

    def load_incremental(self) -> int:
        """Charge la dernière partition silver disponible."""
        partitions = self.list_silver_partitions()
        if not partitions:
            print("[bq_loader] No silver partitions found")
            return 0
        latest = partitions[-1]
        print(f"[bq_loader] Incremental: latest partition = {latest}")
        return self.load_partition(latest)

    def load_backfill(self) -> int:
        """Charge toutes les partitions silver. Retourne le total de lignes."""
        partitions = self.list_silver_partitions()
        if not partitions:
            print("[bq_loader] No silver partitions found")
            return 0
        print(f"[bq_loader] Backfill: {len(partitions)} partitions to load")
        total = 0
        for partition in partitions:
            total += self.load_partition(partition)
        print(f"[bq_loader] Backfill complete: {total} rows total")
        return total
