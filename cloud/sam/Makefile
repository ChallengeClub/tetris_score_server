check-dev:
	sam deploy\
	 --no-execute-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=${{ secrets.TETRIS_FRONT_ORIGIN_DEV }} SQSUrl=${{ secretes.TETRIS_SQS_URL_DEV}}

deploy-dev:
	check-dev:
	sam deploy\
	 --no-comfirm-changeset\
	 --no-fail-on-empty-changeset\
	 --parameter-overrides FrontendOrigin=${{ secrets.TETRIS_FRONT_ORIGIN_DEV }} SQSUrl=${{ secretes.TETRIS_SQS_URL_DEV}}