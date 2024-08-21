provider "aws" {
  region = "us-east-1"
}

resource "aws_ecr_repository" "api" {
  name                 = "lambda-api"
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "api_repository_url" {
  value = aws_ecr_repository.api.repository_url
}

output "api_repository_name" {
  value = aws_ecr_repository.api.name
}
