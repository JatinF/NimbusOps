terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# ---------------------------------------------------------------------------
# Input variables
# ---------------------------------------------------------------------------

variable "project_name" {
  description = "Short name for this deployment (used as a prefix)."
  type        = string
  default     = "nimbusops"
}

variable "aws_region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "us-west-2"
}

variable "s3_bucket_suffix" {
  description = "Optional suffix to make the S3 bucket globally unique."
  type        = string
  default     = ""
}

# ---------------------------------------------------------------------------
# Provider configuration
# ---------------------------------------------------------------------------

provider "aws" {
  region = var.aws_region
}

# ---------------------------------------------------------------------------
# Locals
# ---------------------------------------------------------------------------

locals {
  name_prefix = var.project_name
  bucket_name = var.s3_bucket_suffix == "" ? "${var.project_name}-artifacts" : "${var.project_name}-artifacts-${var.s3_bucket_suffix}"
}

# ---------------------------------------------------------------------------
# S3 bucket for model artifacts
# ---------------------------------------------------------------------------

resource "aws_s3_bucket" "artifacts" {
  bucket = local.bucket_name

  tags = {
    Project = var.project_name
  }
}

resource "aws_s3_bucket_versioning" "artifacts_versioning" {
  bucket = aws_s3_bucket.artifacts.id

  versioning_configuration {
    status = "Enabled"
  }
}

# ---------------------------------------------------------------------------
# ECR repository for Docker images
# ---------------------------------------------------------------------------

resource "aws_ecr_repository" "nimbusops" {
  name                 = "${local.name_prefix}-repo"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project = var.project_name
  }
}

# ---------------------------------------------------------------------------
# CloudWatch log group
# ---------------------------------------------------------------------------

resource "aws_cloudwatch_log_group" "nimbusops_logs" {
  name              = "/aws/nimbusops/${var.project_name}"
  retention_in_days = 14

  tags = {
    Project = var.project_name
  }
}
