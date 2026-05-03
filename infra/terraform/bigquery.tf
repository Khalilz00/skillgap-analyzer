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

resource "google_bigquery_table" "offers" {
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "offers"

  # Pas de protection contre la suppression accidentelle pendant le dev
  deletion_protection = false

  time_partitioning {
    type  = "DAY"
    field = "scrape_date"
  }

  clustering = ["rome_code"]

  schema = jsonencode([
    { name = "offer_id",      type = "STRING",    mode = "NULLABLE" },
    { name = "title",         type = "STRING",    mode = "NULLABLE" },
    { name = "created_at",    type = "DATE",      mode = "NULLABLE" },
    { name = "scrape_date",   type = "DATE",      mode = "NULLABLE" },
    { name = "location",      type = "STRING",    mode = "NULLABLE" },
    { name = "seniority",     type = "STRING",    mode = "NULLABLE" },
    { name = "contract_type", type = "STRING",    mode = "NULLABLE" },
    { name = "rome_code",     type = "STRING",    mode = "NULLABLE" },
    { name = "tech_stack",    type = "STRING",    mode = "REPEATED" },
    { name = "company_name",  type = "STRING",    mode = "NULLABLE" },
  ])
}
