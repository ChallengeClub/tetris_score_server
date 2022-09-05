resource "aws_ecs_cluster" "score_evaluation_cluster" {
  name = var.ecs_cluster_score_evaluation_name
}