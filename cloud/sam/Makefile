check:
	sam deploy\
	 --config-env $(ENV)\
	 --no-execute-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL) DynamoDBNewsTableName=tetris_news_table

deploy:
	sam deploy\
	 --config-env $(ENV)\
	 --no-confirm-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL) DynamoDBNewsTableName=tetris_news_table
