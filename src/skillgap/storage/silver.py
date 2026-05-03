import time
from datetime import date
from io import BytesIO

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import storage  # type: ignore[attr-defined]
from google.cloud.exceptions import GoogleCloudError

from skillgap.parsing.schema import ParsedOffer


class StorageError(Exception):
    pass


class GCSSilverStorage:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def write(self, data: list[ParsedOffer], source: str, scrape_date: date) -> None:
        timestamp = int(time.time())
        date_str = scrape_date.isoformat()
        destination_blob_name = f"{source}/date={date_str}/jobs_{timestamp}.parquet"

        blob = self.bucket.blob(destination_blob_name)
        # convert data to df via model_dump()

        df = pd.DataFrame([offer.model_dump() for offer in data])
        # Schéma explicite pour éviter les types inférés cassés (ex: tech_stack
        # devient list<null> quand toutes les listes sont vides dans le batch)
        schema = pa.schema(
            [
                ("offer_id", pa.large_string()),
                ("title", pa.large_string()),
                ("created_at", pa.date32()),
                ("scrape_date", pa.date32()),
                ("location", pa.large_string()),
                ("seniority", pa.large_string()),
                ("contract_type", pa.large_string()),
                ("rome_code", pa.large_string()),
                ("tech_stack", pa.list_(pa.string())),
                ("company_name", pa.large_string()),
            ]
        )
        table = pa.Table.from_pandas(df, schema=schema, preserve_index=False)

        buffer = BytesIO()
        pq.write_table(table, buffer)
        buffer.seek(0)
        try:
            blob.upload_from_file(buffer, content_type="application/octet-stream")
        except GoogleCloudError as e:
            raise StorageError(f"Error occurred while uploading data to GCS: {e}") from e

    def read(self, source: str, scrape_date: date) -> list[ParsedOffer]:
        date_str = scrape_date.isoformat()
        prefix = f"{source}/date={date_str}/"
        blobs = self.bucket.list_blobs(prefix=prefix)
        offers = []
        for blob in blobs:
            try:
                data = blob.download_as_bytes()
                df = pd.read_parquet(BytesIO(data), engine="pyarrow")
                offers.extend(
                    [ParsedOffer.model_validate(row.to_dict()) for _, row in df.iterrows()]
                )
            except GoogleCloudError as e:
                raise StorageError(f"Error occurred while reading data from GCS: {e}") from e
        return offers
