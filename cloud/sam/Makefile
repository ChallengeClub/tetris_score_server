check-dev:
	sam deploy\
	 --no-execute-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=${{ secrets.TETRIS_FRONT_ORIGIN_DEV }} SQSUrl=${{ secretes.TETRIS_SQS_URL_DEV}}

deploy-dev:
	sam deploy\
	 --no-confirm-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=${{ secrets.TETRIS_FRONT_ORIGIN_DEV }} SQSUrl=${{ secretes.TETRIS_SQS_URL_DEV}}