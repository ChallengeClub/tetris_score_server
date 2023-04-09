check-dev:
	sam deploy\
	 --config-env dev\
	 --no-execute-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL)

deploy-dev:
	sam deploy\
	 --config-env dev\
	 --no-confirm-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL)

check-prod:
	sam deploy\
	 --config-env prod\
	 --no-execute-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL)

deploy-prod:
	sam deploy\
	 --config-env prod\
	 --no-confirm-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=$(TETRIS_FRONT_ORIGIN) SQSUrl=$(SQS_URL)
