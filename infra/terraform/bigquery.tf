resource "google_bigquery_dataset" "raw" {
  dataset_id                  = "raw_${var.environment}"
  location                    = "europe-west1"
  default_table_expiration_ms = 90 * 24 * 60 * 60 * 1000
}

resource "google_bigquery_dataset" "staging" {
  dataset_id                  = "staging_${var.environment}"
  location                    = "europe-west1"
  default_table_expiration_ms = 30 * 24 * 60 * 60 * 1000
}

resource "google_bigquery_dataset" "marts" {
  dataset_id = "marts_${var.environment}"
  location   = "europe-west1"
}
