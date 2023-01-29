resource "aws_iam_role" "apigateway_putlog" {
  name = var.api_gateway_putlog_cloudwatch_role

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "apigateway_putlog" {
  role       = aws_iam_role.apigateway_putlog.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_api_gateway_account" "score_evaluation_apigateway_account" {
  cloudwatch_role_arn = aws_iam_role.apigateway_putlog.arn
}

resource "aws_cloudwatch_log_group" "apigateway_accesslog" {
  name = var.api_gateway_cloudwatch_log_group_name
}

resource "aws_cloudwatch_log_group" "ecs_execution_log" {
  name = var.ecs_cloudwatch_log_group_name
}

resource "aws_cloudwatch_metric_alarm" "sqs_waiting_message_alarm" {
  alarm_name          = var.ecs_cloudwatch_scaleout_alarm
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  dimensions = {
    QueueName  = aws_sqs_queue.score_evaluation_queue.name
  }

  alarm_description = "This metric monitors sqs message counts"
  alarm_actions = [
    aws_appautoscaling_policy.ecs_score_evaluation_scaleout_policy.arn,
  ]
  ok_actions = [
    aws_appautoscaling_policy.ecs_score_evaluation_scalein_policy.arn,
  ]
}
