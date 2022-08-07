locals {
  function_name = "api_to_sqs_lambda_function"
}

data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "src"
  output_path = "archive/api_to_sqs_lambda_function_function.zip"
}

data "archive_file" "layer_zip" {
  type        = "zip"
  source_dir  = "lambda_layer/packages"
  output_path = "archive/lambda_layer.zip"
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

data "aws_iam_policy_document" "message_to_sqs_policy_doc" {
  statement {
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.score_evaluation_queue.arn]
  }
}
resource "aws_iam_policy" "send_message_to_sqs_policy" {
  name   = "SendMessageToSQSPolicy"
  policy = data.aws_iam_policy_document.message_to_sqs_policy_doc.json
}
resource "aws_iam_role" "send_message_to_sqs_lambda_role" {
  name               = "SendMessageToSQSLambdaRole"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "attachment" {
  role       = aws_iam_role.send_message_to_sqs_lambda_role.name
  policy_arn = aws_iam_policy.send_message_to_sqs_policy.arn
}

resource "aws_lambda_function" "function" {
  function_name = local.function_name
  handler       = "send_message_to_sqs.lambda_handler"
  role          = aws_iam_role.send_message_to_sqs_lambda_role.arn
  runtime       = "python3.9"
  environment {
    variables = {
      SQS_URL = data.aws_sqs_queue.score_evaluation_queue_data.url
    }
  }

  filename         = data.archive_file.function_source.output_path
  source_code_hash = data.archive_file.function_source.output_base64sha256
  layers           = ["${aws_lambda_layer_version.lambda_layer.arn}"]
}

resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name               = "lambda_layer"
  filename                 = data.archive_file.layer_zip.output_path
  source_code_hash         = data.archive_file.layer_zip.output_base64sha256
  compatible_runtimes      = ["python3.9"]
  compatible_architectures = ["x86_64"]
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.tetris_api.execution_arn}/*/*/score_evaluation"
}
