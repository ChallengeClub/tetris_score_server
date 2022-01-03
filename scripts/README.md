# prepare procedure on server 

## ツールインストール

```
# 既にあればOK
sudo apt install -y git curl

# 追加インストール
sudo apt install -y docker.io
sudo usermod -aG docker ubuntu  # logout/loginによりsudo dockerを不要にする

# 必要に応じて追加
cd /usr/bin/
sudo ln -s python3 python

# 必要に応じて追加
sudo apt-get install -y python3-pip
pip3 install --upgrade pip
pip3 install numpy
pip3 install pyqt5

sudo apt install -y xvfb
export DISPLAY=:1
nohup Xvfb -ac ${DISPLAY} -screen 0 1280x780x24 &
```

```
git clone https://github.com/seigot/tetris
git clone https://github.com/seigot/tetris_score_server
git clone https://github.com/seigot/tetris_game_autotest
```

## 設定ファイル準備

`~/.netrc`

```
machine github.com
login xxxxx
password xxxxx
```

API_KEY

```
echo "export API_KEY=XXXX" >> ~/.bashrc
source ~/.bashrc
```

