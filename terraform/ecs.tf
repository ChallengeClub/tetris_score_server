resource "aws_ecs_cluster" "score_evaluation_cluster" {
  name = var.ecs_cluster_score_evaluation_name
}

resource "aws_ecs_task_definition" "service" {
  family                  = var.ecs_task_definition_family
  requiresCompatibilities = FARGATE
  container_definitions = jsonencode([
    {
      name   = var.ecs_task_definition_family
      image  = var.ecs_task_definition_image
      cpu    = "2048"
      memory = "4GB"
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
    },
  ])
}
