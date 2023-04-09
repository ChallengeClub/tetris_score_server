compile:
	protoc --python_out=. score_evaluation_message.proto
	protoc --pyi_out=. score_evaluation_message.proto

copy:
	cp score_evaluation_message_pb* ../cloud/sam/scripts/post_competition_entry
	cp score_evaluation_message_pb* ../cloud/sam/scripts/post_evaluation_request
	cp score_evaluation_message_pb* ../server/score_evaluation/domain/model
