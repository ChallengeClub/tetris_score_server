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
cloudwatch_role_api_gateway_putlog = "cloudwatch_role_api_gateway_putlog"
cloudwatch_log_group_name          = "score_evaluation_apigateway_accesslog"

/* 
SQS
*/
sqs_score_evaluation_name            = "score-evaluation-queue"
sqs_score_evaluation_deadletter_name = "score-evaluation-deadletter-queue"

/* 
VPC
*/
vpc_cidr                 = "10.0.0.0/21"
vpc_tag                  = "tetris_score_server"
subnet_cidr              = "10.0.0.0/24"
subnet_availability_zone = "ap-northeast-1c"
