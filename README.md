# Easy-Graph-Draw-for-mode-locking-measurement
[ここ](https://github.com/Skey7731/Easy-Graph-Draw-for-Mode-Locking-Measurement-2/releases)からexeファイルをダウンロードして使ってください。  

## スクショ
:::spoiler メインウィンドウ
![image](https://hackmd.io/_uploads/rksRhwPi6.png)
:::
  
:::spoiler グラフウィンドウ(OSA) 
![](https://hackmd.io/_uploads/r1oQqcnPh.png)
:::
  
:::spoiler 一括生成用ウィンドウ
![image](https://hackmd.io/_uploads/H1UbTwvjp.png)
:::

# 説明
OSA、オシロスコープ、スペアナで測定した生データ(txt,csv,setファイル)をグラフに変換して表示、保存などを行なえます。グラフの作成、データ確認などに使ってください。  
ソースコードから動かす場合はPython3.11、Python3.10で動作確認済み。Python3.8だと.txtファイルの読み込みにに失敗するので注意。

# 使用測定機器
- OSA：ANDO AQ6317B
- オシロスコープ：RIGOL DS2202E
- PD：NEW FOCUS, inc. IR 1 GHz Low Noise Photoreciever (正確な型番不明)
- スペアナ：ROHDE＆SCHWARZ FPC1500
- 自己相関計：FEMTOCHROME🄬 RESEARCH, inc. FR-103XL

# 使い方
ウィンドウごとに説明します。  
基本は…  
ボタン押して新しいウィンドウが出てくる→そのウィンドウでグラフ描くor画像保存する
> 使い方はなんとなく分かるように作ったはず…

## **メインウィンドウ**  
:::spoiler 画像
![image](https://hackmd.io/_uploads/S1zkNODsp.png)  
:::
ボタンを押して出てきたウィンドウで各機能を使用してください。  
スペースの都合で全て別ウィンドウで表示されます。  
<kbd>OSAのグラフの表示</kbd>：OSAのグラフウィンドウを生成  
<kbd>パルス波形の表示</kbd>：パルス波形のグラフウィンドウを生成  
<kbd>ESAのグラフの表示</kbd>：ESAのグラフウィンドウを生成  
<kbd>自己相関波形の表示</kbd>：自己相関波形のグラフウィンドウを生成  
<kbd>一括グラフ生成(β版)</kbd>：一括生成用ウィンドウを生成  
  > グラフ表示はしなくていいから、とりあえず全部まとめて画像に変換したい時用  

## **グラフウィンドウ**  
:::spoiler 画像
![](https://hackmd.io/_uploads/r1oQqcnPh.png)
:::
### **共通項目**
- ### 描画  
  - それぞれのグラフウィンドウにファイルをドラッグアンドドロップするか<kbd>ファイルを選択</kbd>を押してデータファイルを選ぶことでグラフの描画/再描画が可能。  ※複数ファイル非対応  
- ### 軸範囲について
  - X軸：データの存在範囲いっぱい
  - Y軸：データの存在範囲から20 %ずつ外側まで
- ### グラフの簡易設定
  - `☑設定を表示`のチェックボックスで表示できます。  
  ![image](https://hackmd.io/_uploads/BycnpDvoT.png)
  - 上段  
  ![image](https://hackmd.io/_uploads/ByL41dvi6.png)
    - 数字の書いてあるボタン(<kbd>0.0</kbd><kbd>1.0</kbd>など)を押すと軸の範囲を変更できる。
    - <kbd>リセット</kbd>ボタンでファイル読み込み時の状態に軸の範囲をリセットできる。
    - `☑固定`にチェックを入れると新しくファイルを読み込んでもX軸やY軸の範囲が変わらなくなる。  
      > もう少し詳細な設定はグラフ下のツールバーから。  
  - 下段  
  ![image](https://hackmd.io/_uploads/r1qoWuwja.png)  
    左から  
    - 重ね書き：チェックを入れると次にデータを読み込んだ際に現在のプロットが消えなくなる。  
    - グリッド線：灰色でグリッド線が描かれる。  
    - 軸ラベル：軸ラベルを表示する。  
    - グラフタイトル：タイトルを表示する。  
    - プロット色：グラフの色を5色から選べる。office製品でつかえるデフォルトの色と同じ色。  
  


  
- ### ツールバー  
  Matplotlibの物とほぼ同じ。  
  ![image](https://hackmd.io/_uploads/rkasADPjp.png)  
   左から
  - 表示リセット
  - 元に戻す
  - やり直し
  - パンと移動
  - 拡大鏡
  - 軸の範囲などの設定
  - 画像保存 

### **ウィンドウごとの項目**
### **OSAグラフウィンドウ (対応ファイル形式: txt, csv)**  
- OSAで測定したスペクトルを表示
- FWHM($\Delta \lambda$)を表示。  
- 換算パルス幅は中心波長1550 nmとして次式を用いて計算。  
$$
t_{p\_conv}=2.52\times 10^{-3}\ \rm{m･s}/\Delta \lambda
$$
- 最大強度を取る点の左右両側に最大強度-3 dBm以下の点がないとFWHMが計算できずエラーになります。  

### **パルス波形グラフウィンドウ - Waveform (対応ファイル形式: csv)**  
- オシロで測定したパルス波形を表示。  
- 複数チャンネルのデータが保存されている場合は`☑CH1`と`☑CH2`でチャンネルを変更して描画可能。

### **ESAグラフウィンドウ (対応ファイル形式: set, csv)**  
- スペアナで測定したRFスペクトルの表示。   
- 複数チャンネルのデータが保存されている場合は`☑CH1`と`☑CH2`でチャンネルを変更して描画可能。`☑ave`で両者の平均値を描画。  
- 繰り返し周波数を計測する目的でピーク周波数を表示。周波数の小さい側から見ていって最初のピークのみ表示。  
  > ただし、0 Hzからプロットしている場合は0 Hzに大きなピークがあるので注意。  

### **自己相関波形グラフウィンドウ (対応ファイル形式: csv)**  
- オシロで測定した自己相関波形の表示。  
- 自己相関幅から近似したパルス幅$t_p$を表示。  
- パルス幅計算の際の近似波形を☑$sech^2$と☑ガウシアンから選択可能。  
  > 多分$sech^2$しか使わない  
- 換算スペクトル幅は中心波長1550 nmとして次式を用いて計算。
$$
\Delta \lambda_{conv}=2.52\times 10^{-3}\ \text{m･s}\ /t_p
$$
- 複数チャンネルのデータが保存されている場合は`☑CH1`と`☑CH2`でチャンネルを変更して描画可能。
- `☑y軸を正規化`にチェックを入れると強度が正規化されて0~1になる。

## 一括生成用ウィンドウ
:::spoiler 画像
![image](https://hackmd.io/_uploads/B1QVI_Pop.png)
:::
- 画像生成手順  
1. ウィンドウにファイルをドラッグ&ドロップするとこんな感じで読み込まれる。(複数まとめて読み込みOK!、追加もOK!)  
![image](https://hackmd.io/_uploads/BJ0qJFPsT.png)  
2. 読み込んだデータの種類(今回はパルス波形)を選択して青くなってるの確認。  
![image](https://hackmd.io/_uploads/Bkcxltwop.png)  
3. <kbd>グラフ変換！</kbd>を押すと画像になって保存される。  
![image](https://hackmd.io/_uploads/Sy65btDiT.png)  
4. <kbd>リセット</kbd>を押すと読み込んだ履歴を消せる。  
![image](https://hackmd.io/_uploads/ryEWZFwia.png)



# スペアナ(ESA)用のソフトはこちら
[R&S® InstrumentView](https://www.rohde-schwarz.com/jp/software/instrumentview/)

これをインストールして ```C:/Program Files (x86)/Rohde-Schwarz/InstrumentView/``` に ```InstrumentView.exe```があればsetファイルをcsvに変換して保存してから表示できます。  
上手くいかなければインストールしたソフトを用いて自分でcsvに変換してください。  

シェルコマンドで下記を実行してcsvに変換しています。  
やりたければコマンドプロンプトで直接もできます。詳しくはネットにあるマニュアルを自分で調べて下さい。

    InstrumentView.exe -ConvertToCSV "myfile.set" "myfile.csv"


