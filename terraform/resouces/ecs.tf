resource "aws_ecs_cluster" "score_evaluation_cluster" {
  name = var.score_evaluation_ecs_cluster_name
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
  name               = var.score_evaluation_ecs_task_execution_role_name
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
      "sqs:DeleteMessage",
      "dynamodb:UpdateItem"
    ]
    resources = [
      aws_sqs_queue.score_evaluation_queue.arn,
      aws_dynamodb_table.dynamodb-table.arn
    ]
  }
}

resource "aws_iam_policy" "score_evaluation_task_policy" {
  name   = var.score_evaluation_ecs_task_role_policy
  policy = data.aws_iam_policy_document.score_evaluation_task_policy_doc.json
}

resource "aws_iam_role" "ecs_task_role" {
  name               = var.score_evaluation_ecs_task_role_name
  assume_role_policy = data.aws_iam_policy_document.ecs_task_assume_role.json
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_policy_attachment" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.score_evaluation_task_policy.arn
}

resource "aws_ecs_task_definition" "score_evaluation_task" {
  family                   = var.score_evaluation_ecs_task_definition_family
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  container_definitions = jsonencode([
    {
      name   = var.score_evaluation_ecs_task_definition_family
      image  = var.score_evaluation_container_image
      cpu    = 1024
      memory = 2048
      environment = [
        {
          "name" : "sqs_url",
          "value" : data.aws_sqs_queue.score_evaluation_queue_data.url
        },
        {
          "name" : "dynamodb_table",
          "value" : var.dynamodb_table_name
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

resource "aws_ecs_service" "score_evaluation_service" {
  name            = var.score_evaluation_ecs_service
  cluster         = aws_ecs_cluster.score_evaluation_cluster.id
  task_definition = aws_ecs_task_definition.score_evaluation_task.arn
  desired_count   = 0
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = [aws_subnet.tetris_score_server_subnet.id]
    assign_public_ip = true
  }
}

resource "aws_appautoscaling_target" "ecs_score_evaluation_autoscaling_target" {
  service_namespace  = "ecs"
  resource_id        = "service/${aws_ecs_cluster.score_evaluation_cluster.name}/${aws_ecs_service.score_evaluation_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  min_capacity       = var.score_evaluation_ecs_service_min_count
  max_capacity       = var.score_evaluation_ecs_service_max_count
}

resource "aws_appautoscaling_policy" "ecs_score_evaluation_scaleout_policy" {
  name               = "scaleout_policy"
  service_namespace  = "ecs"
  policy_type        = "StepScaling"
  resource_id        = "service/${aws_ecs_cluster.score_evaluation_cluster.name}/${aws_ecs_service.score_evaluation_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
 
  step_scaling_policy_configuration {
    adjustment_type         = "ExactCapacity"
    cooldown                = 60
    metric_aggregation_type = "Average"
    # set the desired ecs service count to 1, when cloud watch alarm switches to alarm state
    step_adjustment {
      metric_interval_lower_bound = 0
      scaling_adjustment          = 1
    }
  }
 
  depends_on = [aws_appautoscaling_target.ecs_score_evaluation_autoscaling_target]
}

resource "aws_appautoscaling_policy" "ecs_score_evaluation_scalein_policy" {
  name               = "scalein_policy"
  service_namespace  = "ecs"
  policy_type        = "StepScaling"
  resource_id        = "service/${aws_ecs_cluster.score_evaluation_cluster.name}/${aws_ecs_service.score_evaluation_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
 
  step_scaling_policy_configuration {
    adjustment_type         = "ExactCapacity"
    cooldown                = 60
    metric_aggregation_type = "Average"
    # set the desired ecs service count to 1, when cloud watch alarm switches to ok state
    step_adjustment {
      metric_interval_upper_bound = 0
      scaling_adjustment = 0
    }
  }
  depends_on = [aws_appautoscaling_target.ecs_score_evaluation_autoscaling_target]
}

