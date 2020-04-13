# 強化学習
シミュレーションモデルに対して強化学習アルゴリズムを適用し、フィードバック制御器を設計する。
Open AIの開発したgymとbaselinesを使う。

## インストール
```
sudo apt-get update && sudo apt-get install cmake libopenmpi-dev python3-dev zlib1g-dev python3-pip python3-tk git -y
sudo apt-get install git -y
pip3 install tensorflow==1.12.0 autograd scipy
pip3 install gym==0.12.5
cd ~
git clone https://github.com/openai/baselines.git
cd baselines
git checkout fa37beb52e867dd7bd9ae6cdeb3a5e64f22f8546
pip3 install -e .
pip3 uninstall gym
pip3 install gym==0.12.5
```

## 実行
```
bash run_pendulum.bash
```

* 学習結果は、`result_apply`の中。
* 実機に適用するためには、`result_apply`と`custom_gym`のディレクトリを`test_py.py`のある階層にコピーする。

## 注意
* 別の目的のために作ったプログラムを最小限の書き換えで使っているため、変数名と実態が違うものがある（例えば`max_torque`）。
* gymのrender()描画機能を使った場合には角度・角速度符号の定義が逆（この描画機能を使わなくてもこの課題はできる）。あくまで描画機能だけの問題なので、シミュレーション・制御の内容としては気にする必要はない。

