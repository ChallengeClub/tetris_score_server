resource "aws_sqs_queue" "score_evaluation_queue" {
  name                      = var.score_evaluation_sqs_queue_name
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.score_evaluation_queue_deadletter.arn
    maxReceiveCount     = var.score_evaluation_queue_max_count
  })
}

resource "aws_sqs_queue" "score_evaluation_queue_deadletter" {
  name = var.score_evaluation_sqs_deadletter_queue_name
}

data "aws_sqs_queue" "score_evaluation_queue_data" {
  name = aws_sqs_queue.score_evaluation_queue.name
}