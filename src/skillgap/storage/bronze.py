import json
import time
from datetime import date
from typing import Any

from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError


class StorageError(Exception):
    pass


class GCSBronzeStorage:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def write(self, data: list[dict[str, Any]], source: str, scrape_date: date) -> None:
        json_data = json.dumps(data) if not isinstance(data, str) else data

        date_str = scrape_date.isoformat()
        timestamp = int(time.time())

        destination_blob_name = f"{source}/date={date_str}/jobs_{timestamp}.json"

        blob = self.bucket.blob(destination_blob_name)

        try:
            blob.upload_from_string(json_data, content_type="application/json")
        except GoogleCloudError as e:
            raise StorageError(f"Error occurred while uploading data to GCS: {e}") from e

    def read(self, source: str, scrape_date: date) -> list[dict[str, Any]]:
        date_str = scrape_date.isoformat()
        prefix = f"{source}/date={date_str}/"
        blobs = self.bucket.list_blobs(prefix=prefix)
        offers = []
        for blob in blobs:
            try:
                data = blob.download_as_string()
                offers.extend(json.loads(data))
            except GoogleCloudError as e:
                raise StorageError(f"Error occurred while reading data from GCS: {e}") from e
        return offers
