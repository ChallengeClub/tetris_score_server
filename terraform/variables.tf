/* 
API Gateway
*/
variable "api_gateway_name" {}
variable "api_gateway_stage_name" {}
variable "api_gateway_access_log_format" {}

/* 
Lambda
*/
variable "send_message_to_sqs_function_name" {}
variable "send_message_to_sqs_handler" {}
variable "function_src_dir" {}
variable "function_zip_output_path" {}
variable "layer_src_dir" {}
variable "layer_zip_output_path" {}
variable "lambda_policy_send_message_to_sqs" {}
variable "lambda_role_send_message_to_sqs" {}
variable "lambda_protobuf_layer_name" {}

/* 
CloudWatch
*/
variable "cloudwatch_role_api_gateway_putlog" {}
variable "cloudwatch_api_gateway_log_group_name" {}
variable "cloudwatch_ecs_log_group_name" {}

/* 
SQS
*/
variable "sqs_score_evaluation_name" {}
variable "sqs_score_evaluation_deadletter_name" {}

/* 
ECS
*/
variable "ecs_cluster_score_evaluation_name" {}
variable "ecs_task_definition_family" {}
variable "ecs_task_definition_image" {}
variable "ecs_task_execution_role_name" {}
variable "ecs_task_role_name" {}
variable "ecs_task_role_policy_name" {}
variable "ecs_service_name" {}

/* 
VPC
*/
variable "vpc_cidr" {}
variable "vpc_tag" {}
variable "subnet_cidr" {}
variable "subnet_availability_zone" {}

/* 
dynamodb
*/
variable "dynamodb_table_name" {}
