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