# graphTemplate.py

import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

from matplotlib.figure import Figure
from tkinterdnd2 import *

import sys
sys.path.append('./')
import fileData, settingFrame, usefulModules

# グラフのフォント設定
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 20

class GraphTemplate(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        #-----------------------------------------------
        # データ保存用
        self.file_data = fileData.FileData(['csv','txt','TXT'])

        self.x = []
        self.y = []

        # ファイル名表示
        self.file_text = tk.StringVar()
        self.file_text.set('-ファイル名-')
        file_label = tk.Label(self.master, textvariable=self.file_text)
        file_label.pack()

        # グラフの設定
        self.settings = settingFrame.SettingFrame(self, self.master)

        # matplotlib配置用フレーム
        frame = tk.Frame(self.master, height=420, width=630)
        frame.propagate(False)

        # matplotlibの描画領域の作成
        fig = Figure()

        # 座標軸の作成
        self.ax = fig.add_subplot(1, 1, 1)

        # グラフタイトル設定
        self.ax.set_title('Graph Title', fontsize=22, visible=True)
        
        # 軸ラベル設定
        self.ax.set_xlabel('X Label', visible=True)
        self.ax.set_ylabel('Y Lsbel', visible=True)


        #目盛り、目盛り線の設定
        self.ax.tick_params(
            direction='in',
            top=True,
            right=True
        )
        
        #グラフの余白調節
        fig.subplots_adjust(
            left=0.15,
            bottom=0.18,
            right=0.92,
            top=0.9,
        )

        # matplotlibの描画領域とウィジェット(Frame)の関連付け
        self.fig_canvas = FigureCanvasTkAgg(fig, frame)

        # matplotlibのツールバーを作成
        self.toolbar = usefulModules.my_NavigationToolbar2Tk(self.file_data, self.fig_canvas, frame)

        # matplotlibのグラフをフレームに配置
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, anchor=tk.S)

        # フレームをウィンドウに配置
        frame.pack(expand=True, fill=tk.BOTH)

        # ドラック＆ドロップ導入
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind("<<Drop>>", self.process_droped_file)   

    def draw_graph(self):
        # データがない場合何もしない
        if (not self.file_data.x) and (not self.file_data.y1) and (not self.file_data.y2):
            return

        # プロットの削除
        if self.ax.lines:
            self.ax.lines[0].remove()
    
        # xとyの設定
        self.x = self.file_data.x
        self.y = self.file_data.y1

        # プロット
        self.ax.plot(self.x, self.y)

        # 各種設定の反映
        self.settings.init_settings()
        self.settings.apply_settings()

        # ファイル名を表示
        self.file_text.set(self.file_data.file_name)

        # ウィンドウタイトルをファイル名に
        self.master.title('Graphname {}'.format(self.file_data.file_name))

    # ファイルドロップ時の処理
    def process_droped_file(self, event):
        self.file_data.dnd_get_path(event)  # ファイルの名前やパスを取得
        if self.file_data.file_name:
            tk.messagebox.showinfo('info', '現在のファイル\n' + self.file_data.file_path)
            return
        else:
            tk.messagebox.showinfo('info', 'ファイルを取得できませんでした。\n')
            return
        self.file_data.read_OSA_TXT()       # OSAのtxtファイルとして読み込み
        self.draw_graph()                   # 画面内に新しいグラフの描画

if __name__ == '__main__':
    win = TkinterDnD.Tk()
    app = GraphTemplate(win)
    win.mainloop()
