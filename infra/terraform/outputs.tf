output "bronze_bucket_name" {
  value = google_storage_bucket.bronze.name
}

output "silver_bucket_name" {
  value = google_storage_bucket.silver.name
}

output "artifacts_bucket_name" {
  value = google_storage_bucket.artifacts.name
}

output "raw_dataset_id" {
  value = google_bigquery_dataset.raw.dataset_id
}

output "staging_dataset_id" {
  value = google_bigquery_dataset.staging.dataset_id
}

output "marts_dataset_id" {
  value = google_bigquery_dataset.marts.dataset_id
}

output "worker_service_account_email" {
  value = google_service_account.worker.email
}

output "dbt_service_account_email" {
  value = google_service_account.dbt.email
}
