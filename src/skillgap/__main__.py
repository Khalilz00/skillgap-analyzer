import os

from skillgap.config import BASE_URL, SCOPE, TOKEN_URL
from skillgap.ingestion.auth import FranceTravailAuth
from skillgap.ingestion.client import FranceTravailClient
from skillgap.storage.gcs import GCSBronzeWriter


def main() -> None:
    print("skillgap-analyzer v0.1.0")

    client_id = os.environ["FT_CLIENT_ID"]
    client_secret = os.environ["FT_CLIENT_SECRET"]
    bucket_name = os.environ["GCS_BUCKET_BRONZE"]

    auth = FranceTravailAuth(
        client_id=client_id,
        client_secret=client_secret,
        token_url=TOKEN_URL,
        scope=SCOPE,
    )

    client = FranceTravailClient(auth, BASE_URL)
    results = client.search_jobs("data", 0, 3)

    writer = GCSBronzeWriter(bucket_name)
    writer.write(results, "france_travail")

    print(f"Nombre d'offres récupérées : {len(results)}")
    print("Destination : france_travail")


if __name__ == "__main__":
    main()
