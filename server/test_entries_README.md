# エントリーリポジトリの動作確認機能（test-entries）

## 概要

- 準備したエントリー一覧 csv ファイルに基づいて、順番にエントリーされたリポジトリ、ブランチを clone しスタートコマンドを実行していく
- 実行結果を csv ファイルに上書き、DB 更新

## 手順

1. 大会エントリー状況確認ページ( https://github.com/seigot/tetris_score_server_frontend で url を確認)から csv ファイルをダウンロードする。
2. ダウンロードした csv ファイルを`tetris_score_server/server/`に`entires.csv`として保存する。
3. `tetris_score_server/server/`に移動して`tetris_score_server/server/Makefile`中の`test-entries`を実行する。
   ```
   tetris_score_server/server$ make test-entries
   ```
