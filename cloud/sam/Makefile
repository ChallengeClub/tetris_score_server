check-dev:
	sam deploy\
	 --no-execute-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL)

deploy-dev:
	sam deploy\
	 --no-confirm-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL)