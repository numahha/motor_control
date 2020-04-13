# 開ループ周波数応答（負荷無し）

モータの軸に負荷を取り付けずに、周波数応答を見る。

摩擦などの非線形性の影響を相対的に小さくするためには、できるだけ大きい電流を流す方が好ましい。
しかし、最大回転速度を超えることは好ましくない（のでリミッターが働くようにしている）。
速度の大きさを見つつ指令電圧の大きさを変えながら、周波数応答実験を行う。

* 周期によって適切な指令電圧の大きさは変わる。
* 周期：2s, 1s, 0.5sくらいから様子を見てみる。
* 指令電圧：2.0V（ステップ応答=周期無限大の場合でも最大回転速度以下である）から始めて、少しずつ大きくしていく。


## 試運転をしてみた感想
* 角度について、回転方向に関して偏った結果が出た（なんとなくドリフトしている）。
* 次に、モータドライバ-モータ間の電流の正負を変えて周波数応答実験を行った。この場合についても、同じ方向に偏った結果が出た。
* モータに流す電流の正負を逆にしても同じ方向に偏りが出たため、少なくともモータの回転方向には回りやすい方向と回りにくい方向がありその差が偏りとなって生じていると考えられる（このディレクトリ内にデータを残しておく）。
* 角速度については、回転方向に関する偏りは気にならないと思う。

## 結果
いろんな周波数でやってみて、ボード線図を書いてみてください！
~~プログラム作っただけでちゃんとやってないです。~~

## 注意！
このモータは、研究室に転がっていたものであり、いつ買ってこれまでどのような使い方をしてきたのかも（私にとって）定かではない。
そのため、「この実験結果はモータの品質を評価しているものではない」ということを強調しておく。