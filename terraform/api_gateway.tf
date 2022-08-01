resource "aws_apigatewayv2_api" "tetris_api" {
  name          = "tetris_api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "tetris_api_stage" {
    api_id = aws_apigatewayv2_api.tetris_api.id
    name = "tetris_api_stage"
    auto_deploy = true
}

resource "aws_apigatewayv2_integration" "send_message_to_sqs_lambda_integration" {
    api_id = aws_apigatewayv2_api.tetris_api.id
    integration_uri = aws_lambda_function.function.invoke_arn
    integration_type = "AWS_PROXY"
    integration_method = "POST"
}

resource "aws_apigatewayv2_route" "send_message_lambda" {
  api_id = aws_apigatewayv2_api.tetris_api.id
  route_key = "GET /score_evaluation"
  target = "integrations/${aws_apigatewayv2_integration.send_message_to_sqs_lambda_integration.id}"
}