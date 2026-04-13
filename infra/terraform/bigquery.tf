resource "google_bigquery_dataset" "skillgap" {
  dataset_id                  = "skillgap_${var.environment}"
  location                    = "EU"
  default_table_expiration_ms = 7776000000 # 90 jours en millisecondes
}
