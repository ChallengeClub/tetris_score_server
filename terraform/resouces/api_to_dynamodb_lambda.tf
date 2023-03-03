data "archive_file" "api_to_dynamodb_function_source" {
  type        = "zip"
  source_dir  = var.get_evaluation_results_lambda_src_dir
  output_path = var.get_evaluation_results_lambda_zip_output_path
}

data "archive_file" "api_to_dynamodb_layer_zip" {
  type        = "zip"
  source_dir  = var.get_evaluation_results_lambda_layer_src_dir
  output_path = var.get_evaluation_results_lambda_layer_zip_output_path
}

data "aws_iam_policy_document" "get_result_from_dynamodb_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "get_result_from_dynamodb_policy_doc" {
  statement {
    actions = ["dynamodb:Scan", "dynamodb: GetItem"]
    resources = [
      aws_dynamodb_table.dynamodb-table.arn,
      aws_dynamodb_table.dynamodb-competition-table.arn
    ]
  }
}
resource "aws_iam_policy" "get_result_from_dynamodb_policy" {
  name   = var.get_evaluation_results_lambda_policy
  policy = data.aws_iam_policy_document.get_result_from_dynamodb_policy_doc.json
}
resource "aws_iam_role" "get_result_from_dynamodb_lambda_role" {
  name               = var.get_evaluation_results_lambda_role
  assume_role_policy = data.aws_iam_policy_document.get_result_from_dynamodb_assume_role.json
}

resource "aws_iam_role_policy_attachment" "get_result_from_dynamodb_attachment" {
  role       = aws_iam_role.get_result_from_dynamodb_lambda_role.name
  policy_arn = aws_iam_policy.get_result_from_dynamodb_policy.arn
}

resource "aws_lambda_function" "get_result_from_dynamodb_function" {
  function_name = var.get_evaluation_results_lambda_name
  handler       = var.get_evaluation_results_lambda_handler
  role          = aws_iam_role.get_result_from_dynamodb_lambda_role.arn
  runtime       = "python3.9"
  environment {
    variables = {
      dynamodb_table_name = var.dynamodb_table_name
    }
  }
  filename         = data.archive_file.api_to_dynamodb_function_source.output_path
  source_code_hash = data.archive_file.api_to_dynamodb_function_source.output_base64sha256
  layers           = ["${aws_lambda_layer_version.api_to_dynamodb_lambda_layer.arn}"]
}

resource "aws_lambda_function" "get_result_detail_function" {
  function_name = var.get_result_detail_lambda_name
  handler       = var.get_result_detail_lambda_handler
  role          = aws_iam_role.get_result_from_dynamodb_lambda_role.arn
  runtime       = "python3.9"
  environment {
    variables = {
      dynamodb_table_name = var.dynamodb_table_name
    }
  }
  filename         = data.archive_file.api_to_dynamodb_function_source.output_path
  source_code_hash = data.archive_file.api_to_dynamodb_function_source.output_base64sha256
  layers           = ["${aws_lambda_layer_version.api_to_dynamodb_lambda_layer.arn}"]
}

resource "aws_lambda_function" "get_competition_entries_function" {
  function_name = var.get_competition_entries_lambda_name
  handler       = var.get_competition_entries_lambda_handler
  role          = aws_iam_role.get_result_from_dynamodb_lambda_role.arn
  runtime       = "python3.9"
  environment {
    variables = {
      dynamodb_competition_table_name = var.dynamodb_competition_table_name
    }
  }
  filename         = data.archive_file.api_to_dynamodb_function_source.output_path
  source_code_hash = data.archive_file.api_to_dynamodb_function_source.output_base64sha256
  layers           = ["${aws_lambda_layer_version.api_to_dynamodb_lambda_layer.arn}"]
}

resource "aws_lambda_layer_version" "api_to_dynamodb_lambda_layer" {
  layer_name               = var.get_evaluation_results_lambda_layer_name
  filename                 = data.archive_file.api_to_dynamodb_layer_zip.output_path
  source_code_hash         = data.archive_file.api_to_dynamodb_layer_zip.output_base64sha256
  compatible_runtimes      = ["python3.9"]
  compatible_architectures = ["x86_64"]
}

resource "aws_lambda_permission" "api_to_dynamodb_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_result_from_dynamodb_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.tetris_api.execution_arn}/*/GET/results"
}

resource "aws_lambda_permission" "get_entries_from_dynamodb_lambda_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_competition_entries_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.tetris_api.execution_arn}/*/GET/entries"
}
