# C−Python間の共有メモリ

共有メモリの動作をなんとなく理解する。

## インストール
```
pip3 install sysv_ipc==1.0.1
```

## 使い方
ターミナルで、Cプログラムをコンパイルして実行する。
```
gcc test_c.c
./a.out
```
これは、10秒の`sleep()`関数を待ったあとに自動的に終了するプログラムである。
まずはこのプログラムのみを実行してみる。
共有メモリ（`shared_memory`という名前）に円周率が格納されていて、それが2回printf表示される。


次に、上のCプログラムを実行して`sleep()`関数を待っている最中に、別のターミナルを開いてpythonプログラムを実行する。
```
python3 test_py.py
```
これは、共有メモリの値を読み込み表示し、また別の数値を共有メモリに書き込む。
その結果として、Cプログラムの中の共有メモリ（`shared_memory`という名前）のprintf表示の2回目が、pythonプログラムによって指定された値に変化しているはずである。

## TODO
ftok関数をpythonで使うのは行儀が良くないらしいので、できれば代替案を実装したい。