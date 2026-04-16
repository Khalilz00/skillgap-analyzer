import json
import time
from datetime import datetime
from typing import Any

from google.cloud import storage  # type: ignore[attr-defined]
from google.cloud.exceptions import GoogleCloudError


class StorageError(Exception):
    pass


class GCSBronzeWriter:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def write(self, data: list[dict[str, Any]], source: str) -> None:
        json_data = json.dumps(data) if not isinstance(data, str) else data

        date = datetime.now().strftime("%Y-%m-%d")

        timestamp = int(time.time())

        destination_blob_name = f"{source}/date={date}/jobs_{timestamp}.json"

        blob = self.bucket.blob(destination_blob_name)

        try:
            blob.upload_from_string(json_data, content_type="application/json")
        except GoogleCloudError as e:
            raise StorageError(f"Error occurred while uploading data to GCS: {e}") from e
