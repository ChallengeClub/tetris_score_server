resource "aws_sqs_queue" "score_evaluation_queue" {
  name                      = var.sqs_score_evaluation_name
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.score_evaluation_queue_deadletter.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "score_evaluation_queue_deadletter" {
  name = var.sqs_score_evaluation_deadletter_name
}

data "aws_sqs_queue" "score_evaluation_queue_data" {
  name = aws_sqs_queue.score_evaluation_queue.name
}