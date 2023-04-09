output "sqs_url" {
  value     = data.aws_sqs_queue.score_evaluation_queue_data.url
  sensitive = true
}
