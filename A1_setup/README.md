# セットアップ

## モータ
[RH8-6006-E100DO](https://www.hds.co.jp/products/lineup/rotary/02ra08_rh/)を使う。
「研究室に転がっていたand研究室のロボット実験装置でも用いている」が採用理由。


## I/O ボード
* DA入力ボード[PCI-3343A](http://www.interface.co.jp/catalog/prdc.asp?name=pci-3343a)
* エンコーダカウンタボード[PCI-6205C](http://www.interface.co.jp/catalog/prdc.asp?name=pci-6205c)
「将来的に研究室のロボット実験装置で用いたい」というのが採用理由（この演習自体が実装の練習を目的としている）。


## エンコーダパルス信号の変換
モータが出力するエンコーダパルスは，オープンコレクタ出力／シングルエンド信号となっている（[技術資料](https://www.hds.co.jp/products/dl_technicaldocument/index.html#rotary-rh-001)の2ページより，型番RH8-6006-E100DOの最後のOがオープンコレクタ出力を意味している）．
一方，エンコーダカウンダボードは，[差動入力(RS-422)](http://www.interface.co.jp/catalog/prdc.asp?name=PCI-6205C&phase=spe)の製品である．
[インタフェース社FAQ](http://www.interface.co.jp/support/faq_result.asp?file_name=455&ref=rss)によると，
「シングルエンド信号はそのまま接続することはできません。74LS14などのインバータを使用して反転信号を作り、反転と非反転信号を接続する必要があります」と書いてあり，同様の対応をする必要がある．

オシロスコープを使ってでオープンコレクタ出力信号の電圧差を見ると，5V程度だった．
また，PCI-6205Cのユーザマニュアル（閲覧にはアカウントが必要）の30ページを見ると，入力信号電圧範囲が0-5V，Highレベル入力電圧が2Vと書いてある．
そのため，オープンコレクタ出力信号をそのまま差動入力のプラス側に，オープンコレクタ出力信号の反転を差動入力のマイナス側に繋げば対応できると考えられる．

オープンコレクタ出力信号の反転を作るためのインバータとして，[TC74HC04AP](https://toshiba.semicon-storage.com/jp/product/logic/cmos-logic/detail.TC74HC04AP.html)
を用いる（ちなみに，「研究室に十分な個数転がっていた」が採用理由）．
なお，技術資料を確認すれば，電源電圧Vcc=-0.5～7，入力電圧Vin=-0.5～Vcc+0.5，出力電圧Vin=-0.5～Vcc+0.5（単位は全てボルト）より，上記の条件（入力と5V程度）を満たしていることが分かる．


## ソフトウェア環境
* Ubuntu 18にインタフェース社のドライバをインストールして用いる。[インストール方法はここを参照](https://github.com/numahha/interface_ubuntu18)
* 簡単のため，RT-preemptを使ったリアルタイム制御は無しとする（この演習のみ）。


## PC（この演習のみ）
上のソフトウェアが動きさえすれば何でも良い。


## サーボドライバ（この演習のみ）
[サーボランド株式会社　DCサーボモータドライバ　サーボモジュール SMCシリーズ AIタイプ（アナログ指令）](http://www.servoland.co.jp/products/price.html#SMC)を使う。
電流制御モードで用いる。調整方法はA2で述べる。
「研究室に転がっていた」が採用理由。

## エンコーダ電源（この演習のみ）
[モータ技術資料17ページ](https://www.hds.co.jp/products/dl_technicaldocument/index.html#rotary-rh-001)より、5-12Vで60mA相当の電源をエンコーダに供給する必要がある。

●●●USBから供給するやつを作る。


## 土台（この演習のみ）
（[モータ技術資料20ページ](https://www.hds.co.jp/products/dl_technicaldocument/index.html#rotary-rh-001)の）の外形寸法図を見ながら作る．

●●●このディレクトリ内に，各部品の寸法をpdfで置いておく．


## おもり（この演習のみ）

550g,30cm×20cmの板。
板の中心に回転軸を取り付ける場合（C）と、板の角に近い場所に回転軸を取り付ける場合（D）で、2通りを扱う。

[モータ技術資料](https://www.hds.co.jp/products/data/pdf/technicaldocument/rotary/RH_Series_supermini_manual_ja_0104-4R-TRH.pdf)より、許容ラジアル荷重は20kgf (196N)なので、500g程度のものなら問題なく取り付けられる。

a×bで質量Mの板の中心周りの慣性モーメントは、I=(1/12)×M×(a^2+b^2)である。
具体値を計算すると、I=0.0059583(Kg×m^2)となる。

平行軸の定理より、距離d離れた位置での慣性モーメントは、I'=I+Md^2である。
具体値を計算すると、550gで15cm離れる場合、Md^2=0.012375(Kg×m^2)であるため、
I'=0.0183333(Kg×m^2)となる。


