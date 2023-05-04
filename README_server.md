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
## ＝＝[SAM](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/what-is-sam.html)＝＝

AWSリソースの内、サーバレスサービス（Lambda、API Gateway）の管理はSAMで行っています。
### インストール
[ダウンロードページ](https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/install-sam-cli.html)に従ってそれぞれの開発環境に沿ったソースをダウンロード、インストールしてください。

### 初期化
`cloud/sam`フォルダに移動したのち、
```
sam init
```

## ＝＝[Terraform](https://www.terraform.io/)＝＝
AWSのリソースの内、SAMで管理しているリソース以外の管理はTerraformで行っています。  
### インストール
[ダウンロードページ](https://www.terraform.io/downloads)に従ってそれぞれの開発環境に沿ったソースをダウンロード、インストールしてください。

### 初期化
`cloud/terraform`フォルダに移動したのち、
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