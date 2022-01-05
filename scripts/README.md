# prepare procedure on server 

## ツールインストール

```
# 既にあればOK
sudo apt install -y git curl

# 追加インストール
sudo apt install -y jq
sudo apt install -y docker.io
sudo usermod -aG docker ubuntu  
### logout/loginによりsudo dockerを不要にする設定を有効にする
```

## 設定ファイル準備

`~/.netrc` (github.comにアクセスするための)

```
machine github.com
login xxxxx
password xxxxx
```

`git config` (git commitするための)

```
## 例
git config --global user.email "s.takada.3o3@gmail.com"
git config --global user.name "seigot"
```

API_KEY (google spread sheetにアクセスするための)

```
echo "export API_KEY=XXXX" >> ~/.bashrc
source ~/.bashrc
```

### swapの設定

必要に応じてやる。以下を参考にする。
> [NTTPCのVPS「Indigo」でスワップの設定](https://qiita.com/mmmmmmmmmmmmm/items/7e6648ecb6874441f995)

```
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
```

`/etc/fstab`の設定

```
# vi /etc/fstab
LABEL=cloudimg-rootfs   /        ext4   defaults        0 0
LABEL=UEFI      /boot/efi       vfat    defaults        0 0
# add here
/swapfile       swap    swap    defaults        0 0
```

```
sudo swapon -a              # -aで/etc/fstabの内容にしたがってスワップを有効にします
free -h                     # swapが有効になっていることを確認mする
```

## 実行

関係するリポジトリ、ファイルを準備する

```
git clone https://github.com/seigot/tetris
git clone https://github.com/seigot/tetris_score_server
cd tetris_score_server/log
```

```
# google spread sheet上のどの行まで評価を進めたかを格納するファイル
# 適切な値に設定する、初めからする場合は"0"を設定する
echo 0 >> current_idx.txt
```

main処理を実行

```
# 本番の場合
nohup bash gameserver.sh -m RELEASE &
# debugの場合
bash gameserver.sh -m DEBUG
```

処理停止する場合は、`process kill`する

```
## process kill する時の例
$ ps -aux | grep bash 
ubuntu     44970  0.0  0.1   9004  3884 ?        S    Jan03   0:00 bash gameserver.sh
$ kill 44970
```
