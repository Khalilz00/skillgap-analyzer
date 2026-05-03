import time
from datetime import date
from io import BytesIO

import pandas as pd
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
        buffer = BytesIO()
        df.to_parquet(buffer, engine="pyarrow", index=False)
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
