/* 
API Gateway
*/
variable "api_gateway_name" {
    type = string
    default = "tetris_api"
}
variable "api_gateway_stage_name" {
    type = string
    default = "tetris_api_stage"
}
variable "api_gateway_access_log_format" {
    type = string
    default = "$context.identity.sourceIp $context.identity.caller $context.identity.user [$context.requestTime] \"$context.httpMethod $context.resourcePath $context.protocol\" $context.status $context.responseLength $context.requestId"
}
variable "api_gateway_allow_origins" {
    type = list
    sensitive = true
}


/* 
Lambda
*/
variable "register_evaluation_request_lambda_name" {
    type = string
    default = "register_evaluation_request"
}
variable "register_evaluation_request_lambda_handler" {
    type = string
    default = "register_evaluation_request.lambda_handler"
}
variable "register_evaluation_request_lambda_src_dir" {
    type = string
    default = "../../scripts/api_to_sqs_lambda/src"
}
variable "register_evaluation_request_lambda_zip_output_path" {
    type = string
    default = "../../archive/register_evaluation_request_lambda.zip"
}
variable "register_evaluation_request_lambda_layer_src_dir" {
    type = string
    default = "../../scripts/api_to_sqs_lambda/layer/packages"
}
variable "register_evaluation_request_lambda_layer_zip_output_path" {
    type = string
    default = "../../archive/register_evaluation_request_lambda_layer.zip"
}
variable "register_evaluation_request_lambda_policy" {
    type = string
    default = "SendMessageToSQSPolicy"
}
variable "register_evaluation_request_lambda_role" {
    type = string
    default = "SendMessageToSQSRole"
}
variable "register_evaluation_request_lambda_layer_name" {
    type = string
    default = "register_evaluation_request_lambda_layer"
}
variable "entry_competition_lambda_name" {
    type = string
    default = "entry_competition_lambda"
}
variable "entry_competition_lambda_handler" {
    type = string
    default = "entry_competition_request.lambda_handler"
}

variable "get_evaluation_results_lambda_name" {
    type = string
    default = "get_evaluation_results_lambda"
}
variable "get_evaluation_results_lambda_handler" {
    type = string
    default = "get_result_from_dynamodb.lambda_handler"
}
variable "get_result_detail_lambda_name" {
    type = string
    default = "get_result_detail_from_dynamodb_lambda"
}
variable "get_result_detail_lambda_handler" {
    type = string
    default = "get_result_detail_from_dynamodb.get_result_detail"
}
variable "get_competition_entries_lambda_name" {
    type = string
    default = "get_competition_entries_lambda"
}
variable "get_competition_entries_lambda_handler" {
    type = string
    default = "get_entries_from_dynamodb.lambda_handler"
}
variable "get_evaluation_results_lambda_src_dir" {
    type = string
    default = "../../scripts/api_to_dynamodb_lambda/src"
}
variable "get_evaluation_results_lambda_zip_output_path" {
    type = string
    default = "../../archive/get_evaluation_results_lambda.zip"
}
variable "get_evaluation_results_lambda_layer_name" {
    type = string
    default = "get_evaluation_results_lambda_layer"
}
variable "get_evaluation_results_lambda_layer_src_dir" {
    type = string
    default =  "../../scripts/api_to_dynamodb_lambda/layer/packages"
}
variable "get_evaluation_results_lambda_layer_zip_output_path" {
    type = string
    default = "../../archive/get_evaluation_results_lambda_layer.zip"
}
variable "get_evaluation_results_lambda_policy" {
    type = string
    default = "GetResultsFromDynamoDBPolicy"
}
variable "get_evaluation_results_lambda_role" {
    type = string
    default = "GetResultsFromDynamoDBLambdaRole"
}


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
