# 参考スコア

（注）乱数の影響により多少のばらつきあり<br>

|     |  level1  |  level2  |  level3  |  自由部門  |
| --- | --- | --- | --- |   -  |
|  random  |  -916  |  -731  |  -4948  |  -  |
|  sample(python start.py -m sample)  |  6935  |  6259  |  3737  |  -  |
|  [kyadさん作の無限テトリス](https://github.com/kyad/tetris/blob/forever-branch/forever.md)  |  -  |  -  |  -  |  20592  |
|  理論値  |  23400+落下ボーナス  |  -  |  -  |  -  |

理論値は「（全てI字の棒が出るなどして）全て4ライン消しをした場合」を想定。<br>
計算式：(制限時間 180(s))÷(テトリス1回に掛かる時間 10(s))×1300点 = 23400点<br>
