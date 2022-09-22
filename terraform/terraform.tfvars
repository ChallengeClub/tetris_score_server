/* 
API Gateway
*/
api_gateway_name              = "tetris_api"
api_gateway_stage_name        = "tetris_api_stage"
api_gateway_access_log_format = "$context.identity.sourceIp $context.identity.caller $context.identity.user [$context.requestTime] \"$context.httpMethod $context.resourcePath $context.protocol\" $context.status $context.responseLength $context.requestId"

/* 
Lambda
*/
send_message_to_sqs_function_name = "lambda_send_message_to_sqs_function"
send_message_to_sqs_handler       = "send_message_to_sqs.lambda_handler"
function_src_dir                  = "../scripts/api_to_sqs_lambda/src"
function_zip_output_path          = "archive/api_to_sqs_lambda_function.zip"
layer_src_dir                     = "../scripts/api_to_sqs_lambda/layer/packages"
layer_zip_output_path             = "archive/layer.zip"
lambda_policy_send_message_to_sqs = "SendMessageToSQSPolicy"
lambda_role_send_message_to_sqs   = "SendMessageToSQSLambdaRole"
lambda_protobuf_layer_name        = "lambda_protobuf_layer"

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
ecs_task_definition_role_name     = "ecsTaskExecutionRole"

/* 
VPC
*/
vpc_cidr    = "10.0.0.0/21"
subnet_cidr = "10.0.0.0/24"
subnet_tag  = "tetris_score_server_subnet"
