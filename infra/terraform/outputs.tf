output "bronze_bucket_name" {
  value = google_storage_bucket.bronze.name
}

output "silver_bucket_name" {
  value = google_storage_bucket.silver.name
}

output "artifacts_bucket_name" {
  value = google_storage_bucket.artifacts.name
}

output "bigquery_dataset_id" {
  value = google_bigquery_dataset.skillgap.dataset_id
}

output "worker_service_account_email" {
  value = google_service_account.worker.email
}
