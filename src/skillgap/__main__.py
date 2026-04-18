import os
from datetime import UTC, datetime, timedelta
from typing import Any

from skillgap.config import BASE_URL, SCOPE, TOKEN_URL
from skillgap.ingestion.auth import FranceTravailAuth
from skillgap.ingestion.client import FranceTravailClient
from skillgap.storage.gcs import GCSBronzeWriter


# function to fetch job offers from France Travail API, date range is optional,
# if not provided, it will fetch all offers
def fetch_job_offers(
    client: FranceTravailClient,
    query: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> list[dict[str, Any]]:
    total_objects, results = client.search_jobs(
        query, 0, 149, start_date=start_date, end_date=end_date
    )
    total_calls = (total_objects + 149) // 150
    for i in range(1, total_calls):
        range_start = i * 150
        range_end = range_start + 149
        _, batch = client.search_jobs(
            query, range_start, range_end, start_date=start_date, end_date=end_date
        )
        results.extend(batch)
    return results


def main() -> None:
    print("skillgap-analyzer v0.1.0")

    client_id = os.environ["FT_CLIENT_ID"]
    client_secret = os.environ["FT_CLIENT_SECRET"]
    bucket_name = os.environ["GCS_BUCKET_BRONZE"]
    # INGESTION_MODE can be "backfill" or "incremental" , default is "incremental"
    ingestion_mode = os.environ.get("INGESTION_MODE", "incremental").lower()

    auth = FranceTravailAuth(
        client_id=client_id,
        client_secret=client_secret,
        token_url=TOKEN_URL,
        scope=SCOPE,
    )

    client = FranceTravailClient(auth, BASE_URL)

    # print mode
    print(f"Ingestion mode: {ingestion_mode}")

    if ingestion_mode == "backfill":
        results = fetch_job_offers(client, "data")
    elif ingestion_mode == "incremental":
        # calcul des dates ici, juste quand on en a besoin
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        yesterday = (datetime.now(UTC) - timedelta(days=1)).strftime("%Y-%m-%d")
        today_iso = f"{today}T00:00:00Z"
        yesterday_iso = f"{yesterday}T00:00:00Z"
        results = fetch_job_offers(client, "data", start_date=yesterday_iso, end_date=today_iso)
    else:
        raise ValueError(
            f"Unknown INGESTION_MODE: {ingestion_mode}. Expected 'backfill' or 'incremental'."
        )

    writer = GCSBronzeWriter(bucket_name)
    writer.write(results, "france_travail")

    print(f"Nombre d'offres récupérées : {len(results)}")
    print("Destination : france_travail")


if __name__ == "__main__":
    main()
