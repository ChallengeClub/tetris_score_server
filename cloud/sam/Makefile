check:
	sam deploy\
	 --config-env $(ENV)\
	 --no-execute-changeset\
	 --no-fail-on-empty-changeset\
	 --resolve-image-repos\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL) DynamoDBNewsTableName=tetris_news_table DynamoDBTrainingTableName=tetris_training_table TetrisTrainingBucketName=$(TETRIS_TRAINING_BUCKET_NAME)

deploy:
	sam deploy\
	 --config-env $(ENV)\
	 --no-confirm-changeset\
	 --no-fail-on-empty-changeset\
	 --resolve-image-repos\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL) DynamoDBNewsTableName=tetris_news_table DynamoDBTrainingTableName=tetris_training_table TetrisTrainingBucketName=$(TETRIS_TRAINING_BUCKET_NAME)
