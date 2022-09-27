resource "aws_ecs_cluster" "score_evaluation_cluster" {
  name = var.ecs_cluster_score_evaluation_name
}

data "aws_iam_policy_document" "ecs_exec_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_execution_role" {
  name               = var.ecs_task_execution_role_name
  assume_role_policy = data.aws_iam_policy_document.ecs_exec_assume_role.json
}

resource "aws_iam_role_policy_attachment" "ecs_ececution_role_policy_attachment" {
  role       = aws_iam_role.ecs_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

data "aws_iam_policy_document" "ecs_task_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "score_evaluation_task_policy_doc" {
  statement {
    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage"
    ]
    resources = [aws_sqs_queue.score_evaluation_queue.arn]
  }
}

resource "aws_iam_policy" "score_evaluation_task_policy" {
  name   = var.ecs_task_role_policy_name
  policy = data.aws_iam_policy_document.score_evaluation_task_policy_doc.json
}

resource "aws_iam_role" "ecs_task_role" {
  name               = var.ecs_task_role_name
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume_role.json
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_policy_attachment" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.score_evaluation_task_policy.arn
}

resource "aws_ecs_task_definition" "score_evaluation_task" {
  family                   = var.ecs_task_definition_family
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  container_definitions = jsonencode([
    {
      name   = var.ecs_task_definition_family
      image  = var.ecs_task_definition_image
      cpu    = 1024
      memory = 2048
      environment = [
        {
          "name" : "sqs_url",
          "value" : data.aws_sqs_queue.score_evaluation_queue_data.url
        }
      ]
      logConfiguration = {
        logDriver = "awslogs",
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_execution_log.name,
          awslogs-region        = "ap-northeast-1",
          awslogs-stream-prefix = "ecsTasklogs"
        }
      }
    }
  ])
}
