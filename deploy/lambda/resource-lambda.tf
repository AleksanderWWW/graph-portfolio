resource "aws_cloudwatch_log_group" "api" {
  name              = "/aws/lambda/api"
  retention_in_days = 14
}

resource "aws_lambda_function" "api" {
  function_name    = "api"
  role             = aws_iam_role.lambda.arn
  image_uri        = "${aws_ecr_repository.api.repository_url}:${var.image_tag}"
  package_type     = "Image"
  source_code_hash = trimprefix(data.aws_ecr_image.image.id, "sha256:")
  timeout          = 10

  environment {
    variables = {}
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
    aws_cloudwatch_log_group.api,
  ]
}

data "aws_ecr_image" "image" {
  repository_name = var.repository_name
  image_tag       = var.image_tag
}
