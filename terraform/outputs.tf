output "api_endpoint_url" {
  value     = aws_apigatewayv2_stage.tetris_api_stage.invoke_url
  sensitive = true
}

output "sqs_url" {
  value     = data.aws_sqs_queue.score_evaluation_queue_data.url
  sensitive = true
}
