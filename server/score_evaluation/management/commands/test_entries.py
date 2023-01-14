# -*- coding:utf-8 -*-

from django.core.management.base import BaseCommand

from ...usecase.test_entries_evaluation_usecase import TestEntriesEvaluationUsecase


# python manage.py から呼び出す自作コマンドを登録するためのクラス
class Command(BaseCommand):
    # python manage.py help test_entriesで表示されるメッセージ
    help = 'execute entry test on given csv'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', nargs=1, type=str)

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        csv_path = options["csv_path"][0]
        testEntriesEvaluationUsecase = TestEntriesEvaluationUsecase()
        testEntriesEvaluationUsecase.execute(csv_path)