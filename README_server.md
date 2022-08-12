# tetris_score_server

スコアアタック用サーバ for https://github.com/seigot/tetris  

# 使い方
## 専用サイトからのプログラム提出（開発中です）
専用webサイトを用意しているので、必要項目を埋めて提出してください  
[開発中webサイト](https://dnj6pabv7wx0g.cloudfront.net/)←まだなにもできません  
[開発中repository](https://github.com/seigot/tetris_score_server_frontend)

## API経由を使ったプログラム提出（開発中です）
[protocol buffers](https://developers.google.com/protocol-buffers)をテンプレートとして用いたプログラム提出用のAPIを開発しております。  
`https://[未公開です].execute-api.ap-northeast-1.amazonaws.com/tetris_api_stage/score_evaluation`  

### --protocol bufffersの導入とAPI提出のテンプレート生成--
[protobuf CLIのインストール](https://github.com/protocolbuffers/protobuf#protocol-compiler-installation)を行ったのち、  
[.protoファイル](protobuf\score_evaluation_message.proto)をダウンロードしてそれぞれの開発言語に沿ったコンパイルファイルを作成してご利用ください。[参考ドキュメント](https://developers.google.com/protocol-buffers/docs/tutorials)  
コンパイルの例↓  
```
protoc --python_out=[コンパイルファイルの出力先] [.protoファイルの格納フォルダ]/score_evaluation_message.proto
```

# 開発環境構築
## .envファイルの準備
本プロジェクトのルートに`.env`ファイルを作成し、
```
# djangoローカルのホスティングポート設定
WEB_SERVER_PORT=8000

# 開発者からシークレットキーを共有してもらうシークレットキー
DJANGO_SECRET_KEY={djangoのシークレットキー}  
```
を記載してください。
## ＝＝[AWS CLI](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-chap-getting-started.html)＝＝
[ドキュメント](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-chap-getting-started.html)を参考にして、AWS CLIを[ダウンロードページ](https://aws.amazon.com/jp/cli/)からダウンロードし、割り当てられたAWS IAMユーザーを用いて認証情報を設定して下さい。  
## ＝＝[Terraform](https://www.terraform.io/)＝＝
AWSのリソース管理はTerraformで行っています。  
### インストール
[ダウンロードページ](https://www.terraform.io/downloads)に従ってそれぞれの開発環境に沿ったソースをダウンロード、インストールしてください。

### 初期化
`/terraform`フォルダに移動したのち、
```
terraform init
```
S3へtfstateファイルを同期させるか聞かれるので`yes`と答える。

## ＝＝[Protocol buffers](https://developers.google.com/protocol-buffers)＝＝
[ダウンロードページ](https://github.com/protocolbuffers/protobuf#protocol-compiler-installation)に従ってそれぞれの開発環境に沿ったソースをダウンロード、インストールしてください。  

## ＝＝[Docker](https://www.docker.com/)＝＝
[ダウンロードページ](https://docs.docker.com/engine/install/)に従ってそれぞれの開発環境に沿ったソースをダウンロード、インストールしてください。 
本プロジェクトのルートディレクトリに移動して、
```
docker-compose up
```
を実行し、サーバ用のコンテナを実行

http://localhost:8000 をブラウザで開き、テストページが表示されることを確認する。