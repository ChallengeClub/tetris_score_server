# -*- coding:utf-8 -*-

from django.core.management.base import BaseCommand

from ...usecase.score_evaluation_application import ScoreEvaluationApplication


# python manage.py から呼び出す自作コマンドを登録するためのクラス
class Command(BaseCommand):
    # python manage.py help pollingで表示されるメッセージ
    help = 'polling sqs and execute score_evaluations'

    def add_arguments(self, parser):
        parser.add_argument('interval', nargs='?', type=int, default=60)

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        interval = options["interval"]
        score_evaluation_application = ScoreEvaluationApplication()
        score_evaluation_application.start(time=interval)