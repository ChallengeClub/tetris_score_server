check:
	sam deploy\
	 --config-env $(ENV)\
	 --no-execute-changeset\
	 --no-fail-on-empty-changeset\
	 --resolve-image-repos\
	 --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) \SQSUrl=$(SQS_URL) DynamoDBNewsTableName=tetris_news_table DynamoDBTrainingTableName=tetris_training_table TetrisTrainingBucketName=$(TETRIS_TRAINING_BUCKET_NAME) SQSName=score_evaluation_queue DynamoDBTableName=tetris_score_results_table DynamoDBCompetitionTableName=tetris_competition_entry_table

deploy:
	sam deploy\
	 --config-env $(ENV)\
	 --no-confirm-changeset\
	 --no-fail-on-empty-changeset\
	 --resolve-image-repos\
	 --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL) DynamoDBNewsTableName=tetris_news_table DynamoDBTrainingTableName=tetris_training_table TetrisTrainingBucketName=$(TETRIS_TRAINING_BUCKET_NAME) SQSName=score_evaluation_queue DynamoDBTableName=tetris_score_results_table DynamoDBCompetitionTableName=tetris_competition_entry_table
