data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = var.register_evaluation_request_lambda_src_dir
  output_path = var.register_evaluation_request_lambda_zip_output_path
}

data "archive_file" "layer_zip" {
  type        = "zip"
  source_dir  = var.register_evaluation_request_lambda_layer_src_dir
  output_path = var.register_evaluation_request_lambda_layer_zip_output_path
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
    actions = [
      "sqs:SendMessage",
      "dynamodb:PutItem"
    ]
    resources = [
      aws_sqs_queue.score_evaluation_queue.arn,
      aws_dynamodb_table.dynamodb-table.arn,
      aws_dynamodb_table.dynamodb-competition-table.arn
    ]
  }
}
resource "aws_iam_policy" "send_message_to_sqs_policy" {
  name   = var.register_evaluation_request_lambda_policy
  policy = data.aws_iam_policy_document.message_to_sqs_policy_doc.json
}
resource "aws_iam_role" "send_message_to_sqs_lambda_role" {
  name               = var.register_evaluation_request_lambda_role
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "attachment" {
  role       = aws_iam_role.send_message_to_sqs_lambda_role.name
  policy_arn = aws_iam_policy.send_message_to_sqs_policy.arn
}

resource "aws_lambda_function" "function" {
  function_name = var.register_evaluation_request_lambda_name
  handler       = var.register_evaluation_request_lambda_handler
  role          = aws_iam_role.send_message_to_sqs_lambda_role.arn
  runtime       = "python3.9"
  environment {
    variables = {
      SQS_URL             = data.aws_sqs_queue.score_evaluation_queue_data.url
      DYNAMODB_TABLE_NAME = var.dynamodb_table_name
    }
  }

  filename         = data.archive_file.function_source.output_path
  source_code_hash = data.archive_file.function_source.output_base64sha256
  layers           = ["${aws_lambda_layer_version.lambda_layer.arn}"]
}

resource "aws_lambda_function" "entry_competition_function" {
  function_name = var.entry_competition_lambda_name
  handler       = var.entry_competition_lambda_handler
  role          = aws_iam_role.send_message_to_sqs_lambda_role.arn
  runtime       = "python3.9"
  environment {
    variables = {
      DYNAMODB_COMPETITION_TABLE_NAME = var.dynamodb_competition_table_name
    }
  }

  filename         = data.archive_file.function_source.output_path
  source_code_hash = data.archive_file.function_source.output_base64sha256
  layers           = ["${aws_lambda_layer_version.lambda_layer.arn}"]
}

resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name               = var.register_evaluation_request_lambda_layer_name
  filename                 = data.archive_file.layer_zip.output_path
  source_code_hash         = data.archive_file.layer_zip.output_base64sha256
  compatible_runtimes      = ["python3.9"]
  compatible_architectures = ["x86_64"]
}

resource "aws_lambda_permission" "permission_apigw_score_evaluation_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.tetris_api.execution_arn}/*/POST/score_evaluation"
}

resource "aws_lambda_permission" "permission_apigw_entry_competition_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.entry_competition_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.tetris_api.execution_arn}/*/POST/entry"
}
