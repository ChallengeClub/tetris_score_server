/* 
CloudWatch
*/
variable "api_gateway_putlog_cloudwatch_role" {
    type = string
    default = "tetris_api_gateway_putlog_cloudwatch_role"
}
variable "api_gateway_cloudwatch_log_group_name" {
    type = string
    default = "tetris_api_gateway_cloudwatch_log_group"
}
variable "ecs_cloudwatch_log_group_name" {
    type = string
    default = "tetris_ecs_cloudwatch_log_group"
}
variable "ecs_cloudwatch_scaleout_alarm" {
    type = string
    default = "sqs_waiting_and_in_evaluation_message_alarm"
}


/* 
SQS
*/
variable "score_evaluation_sqs_queue_name" {
    type = string
    default = "score_evaluation_queue"
}
variable "score_evaluation_sqs_deadletter_queue_name" {
    type = string
    default = "score_evaluation_deadletter_queue"
}
variable "score_evaluation_queue_max_count" {
    type = number
    default = 3
}

/* 
ECS
*/
variable "score_evaluation_ecs_cluster_name" {
    type = string
    default = "score_evaluation_ecs_cluster"
}
variable "score_evaluation_ecs_task_definition_family" {
    type = string
    default = "score_evaluation_family"
}
variable "score_evaluation_container_image" {
    type = string
}
variable "score_evaluation_ecs_task_execution_role_name" {
    type = string
    default = "ScoreEvaluationECSTaskExecutionRole"
}
variable "score_evaluation_ecs_task_role_name" {
    type = string
    default = "ScoreEvaluationECSTaskRole"
}
variable "score_evaluation_ecs_task_role_policy" {
    type = string
    default = "ScoreEvaluationTaskRolePolicy"
}
variable "score_evaluation_ecs_service" {
    type = string
    default = "score_evaluation_ecs_service"
}
variable "score_evaluation_ecs_service_max_count" {
    type = number
    default = 1
}
variable "score_evaluation_ecs_service_min_count" {
    type = number
    default = 0
}

/* 
VPC
*/
variable "score_evaluation_vpc_cidr" {
    type = string
    default = "10.0.0.0/21"
}
variable "score_evaluation_vpc_tag" {
    type = string
    default = "tetris_score_server_vpc"
}
variable "subnet_cidr" {
    type = string
    default = "10.0.0.0/24"
}
variable "subnet_availability_zone" {
    type = string
    default = "ap-northeast-1c"
}

/* 
dynamodb
*/
variable "dynamodb_table_name" {
    type = string
    default = "tetris_score_results_table"
}
variable "dynamodb_competition_table_name" {
    type = string
    default = "tetris_competition_entry_table"
}
