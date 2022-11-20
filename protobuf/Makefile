compile:
	protoc --python_out=. score_evaluation_message.proto
	protoc --pyi_out=. score_evaluation_message.proto

copy:
	cp score_evaluation_message_pb* ../scripts/api_to_sqs_lambda/src
	cp score_evaluation_message_pb* ../server/score_evaluation/domain/model
