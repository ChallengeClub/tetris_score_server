locals {
  function_name = "api_to_sqs_lambda_function"
}

data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "src"
  output_path = "archive/api_to_sqs_lambda_function_function.zip"
}
data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}
resource "aws_iam_role" "lambda_role" {
  name               = "apiToSQSLambdaRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_lambda_function" "function" {
  function_name = local.function_name
  handler       = "send_message_to_sqs.lambda_handler"
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.9"

  filename         = data.archive_file.function_source.output_path
  source_code_hash = data.archive_file.function_source.output_base64sha256
}