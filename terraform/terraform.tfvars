/* 
API Gateway
*/
api_gateway_name              = "tetris_api"
api_gateway_stage_name        = "tetris_api_stage"
api_gateway_access_log_format = "$context.identity.sourceIp $context.identity.caller $context.identity.user [$context.requestTime] \"$context.httpMethod $context.resourcePath $context.protocol\" $context.status $context.responseLength $context.requestId"

/* 
Lambda
*/
send_message_to_sqs_function_name     = "lambda_send_message_to_sqs_function"
send_message_to_sqs_handler           = "send_message_to_sqs.lambda_handler"
function_src_dir                      = "../scripts/api_to_sqs_lambda/src"
function_zip_output_path              = "archive/api_to_sqs_lambda_function.zip"
layer_src_dir                         = "../scripts/api_to_sqs_lambda/layer/packages"
layer_zip_output_path                 = "archive/layer.zip"
lambda_policy_send_message_to_sqs     = "SendMessageToSQSPolicy"
lambda_role_send_message_to_sqs       = "SendMessageToSQSLambdaRole"
lambda_send_message_to_sqs_layer_name = "lambda_send_message_to_sqs_layer"

get_result_from_dynamodb_function_name            = "lambda_get_results_from_dynamodb_function"
get_result_from_dynamodb_function_handler         = "get_result_from_dynamodb.lambda_handler"
get_result_from_dynamodb_function_src_dir         = "../scripts/api_to_dynamodb_lambda/src"
get_result_from_dynamodb_function_zip_output_path = "archive/get_result_from_dynamodb_lambda_function.zip"
get_result_from_dynamodb_layer_name               = "lambda_get_result_from_dynamodb_layer"
get_result_from_dynamodb_layer_src_dir            = "../scripts/api_to_dynamodb_lambda/layer/packages"
get_result_from_dynamodb_layer_zip_output_path    = "archive/get_result_from_dynamodb_layer.zip"
lambda_policy_get_result_from_dynamodb            = "GetResultsFromDynamoDBPolicy"
lambda_role_get_result_from_dynamodb              = "GetResultsFromDynamoDBLambdaRole"

/* 
CloudWatch
*/
cloudwatch_role_api_gateway_putlog    = "cloudwatch_role_api_gateway_putlog"
cloudwatch_api_gateway_log_group_name = "score_evaluation_apigateway_accesslog"
cloudwatch_ecs_log_group_name         = "score_evaluation_ecs_log"

/* 
SQS
*/
sqs_score_evaluation_name            = "score-evaluation-queue"
sqs_score_evaluation_deadletter_name = "score-evaluation-deadletter-queue"

/* 
ECS
*/
ecs_cluster_score_evaluation_name = "score_evaluation_cluster"
ecs_task_definition_family        = "score_evaluation_family"
ecs_task_definition_image         = "public.ecr.aws/r2u8u6o1/tetris_score_evaluation:latest"
ecs_task_execution_role_name      = "ecsTaskExecutionRole"
ecs_task_role_name                = "scoreEvaluationTaskRole"
ecs_task_role_policy_name         = "scoreEvaluationTaskRolePolicy"
ecs_service_name                  = "score_evaluation_service"

/* 
VPC
*/
vpc_cidr                 = "10.0.0.0/21"
vpc_tag                  = "tetris_score_server"
subnet_cidr              = "10.0.0.0/24"
subnet_availability_zone = "ap-northeast-1c"

/* 
dynamodb
*/
dynamodb_table_name = "tetris_score_table"
