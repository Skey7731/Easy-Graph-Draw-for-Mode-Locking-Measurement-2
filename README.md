# Easy-Graph-Draw-for-mode-locking-measurement
- メインウィンドウ  
  ![](https://i.imgur.com/LfBKZKI.png)  
  
- グラフウィンドウ(OSA)  
  ![](https://i.imgur.com/hjDlLws.png)  

# 説明
OSA、オシロスコープ、スペアナの生データ(txt,csv,setファイル)をPythonのmatplotlibでグラフに変換して表示します。  
Python3.11、Python3.10で動作確認済み。Python3.8だと.txtファイルの読み込みにに失敗するので注意。

## 使用測定機器
- OSA：ANDO AQ6317B
- オシロスコープ：RIGOL DS2202E
- PD：NEW FOCUS, inc. IR 1 GHz Low Noise Photoreciever (正確な型番不明)
- スペアナ：ROHDE＆SCHWARZ FPC1500
- 自己相関計：FEMTOCHROME🄬 RESEARCH, inc. FR-103XL

## 使い方
メインウィンドウとグラフを描画して保存するグラフウィンドウに分かれます。  
メインウィンドウにある4つのボタンを押せば対応するグラフウィンドウを好きなだけ表示できます。

- **グラフウィンドウの共通項目**  
  それぞれのグラフウィンドウにファイルをドラッグアンドドロップするか<kbd>ファイルを選択</kbd>を押してデータファイルを選ぶことでグラフの描画/再描画が可能。  ※複数ファイル非対応  
  グラフの簡易的な設定(↓の画像参照)は```設定を表示```のチェックボックスで表示できます。    
  
  ![](https://i.imgur.com/nU3WOAk.png) 
  
  
  グラフ下のツールバーはMatplotlibの物と基本的に同じ。(拡大縮小や余白の調整など)  
  一番右の```save the figure```のボタンのみ変更してあり、元のデータファイルがあった場所に同じ名前で画像を保存できるようにしています。


- **OSA (対応ファイル形式: txt, csv)**  
  OSAのグラフとFWHMを表示。  
  最大強度を取る点の左右両側に最大強度-3 dBm以下の点がないとFWHMが計算できずエラーになります。 
- **パルス波形 - Waveform (対応ファイル形式: csv)**  
  オシロで測定したパルス波形を表示。  
  複数のチャンネルのデータが保存されている場合はチャンネルの選択可。
- **ESA (対応ファイル形式: set, csv)**  
  スペアナで測定したRFスペクトルの表示。  
  繰り返し周波数を計測する目的でピーク周波数を表示。ただし、0 Hzからプロットしている場合は0 Hzに大きなピークがあるので注意。
- **自己相関波形 - Autocorrelation Waveform (対応ファイル形式: csv)**  
  オシロで測定した自己相関波形の表示。  
  自己相関幅から換算してパルス幅も表示。(sech^2(基本こっちでいい)とガウシアンでの近似に対応)


# スペアナ(ESA)用のソフトはこちら
[R&S® InstrumentView](https://www.rohde-schwarz.com/jp/software/instrumentview/)

これをインストールして ```C:/Program Files (x86)/Rohde-Schwarz/InstrumentView/``` に ```InstrumentView.exe```があればsetファイルをcsvに変換して保存してから表示できます。  
上手くいかなければインストールしたソフトを用いて自分でcsvに変換してください。  

シェルコマンドで下記を実行してcsvに変換しています。  
やりたければコマンドプロンプトで直接もできます。詳しくはネットにあるマニュアルを自分で調べて下さい。

    InstrumentView.exe -ConvertToCSV "myfile.set" "myfile.csv"


