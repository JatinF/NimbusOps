# infrastructure/outputs.tf

output "artifacts_bucket" {
  description = "S3 bucket for NimbusOps model artifacts."
  value       = aws_s3_bucket.artifacts.bucket
}

output "ecr_repository_url" {
  description = "ECR repository URI for NimbusOps Docker images."
  value       = aws_ecr_repository.nimbusops.repository_url
}

output "log_group_name" {
  description = "CloudWatch log group used by NimbusOps services."
  value       = aws_cloudwatch_log_group.nimbusops_logs.name
}
