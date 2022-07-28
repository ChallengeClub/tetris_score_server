resource "aws_sqs_queue" "score_evaluation_queue" {
  name                      = "score-evaluation-queue"
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.score_evaluation_queue_deadletter.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "score_evaluation_queue_deadletter" {
  name = "score-evaluation-deadletter-queue"
}