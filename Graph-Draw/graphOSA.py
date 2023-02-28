# graphOSA.py

import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from matplotlib.figure import Figure
from tkinterdnd2 import *

import sys
sys.path.append('./')
import fileData, settingFrame, usefulModules

# グラフのフォント設定
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 20

class GraphOSA(tk.Frame):
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
        self.file_text.set('-ファイル名-\nFWHM:  nm 換算パルス幅:  ps')
        file_label = tk.Label(self.master, textvariable=self.file_text)
        file_label.pack()

        # グラフの設定(共通)
        self.commom_setting_frame = tk.Frame(self.master, height=1, width=1)
        self.settings = settingFrame.SettingFrame(self, self.commom_setting_frame)
        self.commom_setting_frame.propagate(False)
        self.commom_setting_frame.pack()

        frame_tgl_file = tk.Frame(self.master)  #---------------------------------------------------------------
        # グラフ設定の表示切替(共通)
        self.tgl_set_bln = tk.BooleanVar(value=False)
        self.tgl_set_button = tk.Checkbutton(frame_tgl_file, text='設定を表示', variable=self.tgl_set_bln, command=self.toggle_setting)
        self.tgl_set_button.pack(side='left', padx=[5,0])
        # ファイル選択ボタン(共通)
        file_select_button = tk.Button(frame_tgl_file, text='ファイルを選択', padx=10, command=self.file_select)
        file_select_button.pack(side='right', padx=[0,10], pady=[0,5])
        frame_tgl_file.pack(fill='x')   #-------------------------------------------------------------------------------

        # matplotlib配置用フレーム
        frame = tk.Frame(self.master, height=420, width=630)
        frame.propagate(False)

        # matplotlibの描画領域の作成
        fig = Figure()

        # 座標軸の作成
        self.ax = fig.add_subplot(1, 1, 1)

        # グラフタイトル設定
        self.ax.set_title('Spectrum', fontsize=22, visible=True)
        
        # 軸ラベル設定
        self.ax.set_xlabel('Wavelength / nm', visible=True)
        self.ax.set_ylabel('Intensity / dBm', visible=True)


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

        # FWHMの計算
        plot_li =[]
        for i in range(len(self.x)):
            plot_li.append([self.x[i], self.y[i]])

        FWHM = usefulModules.calc_FWHM(plot_li, 'dB', 3)
        if FWHM[1]:
            conv_pulse_width = 2.52 / FWHM[0]
            self.file_text.set('{}\nFWHM: {:.3f} nm  換算パルス幅: {:.3f} ps'.format(self.file_data.file_name, FWHM[0], conv_pulse_width))
        else:
            self.file_text.set(self.file_data.file_name + '\nFWHM: error  換算パルス幅:  ps')

        # ウィンドウタイトルの設定
        self.master.title('OSA ' + self.file_data.file_path)

    # ファイルドロップ時の処理
    def process_droped_file(self, event):
        self.file_data.dnd_get_path(event)  # ファイルの名前やパスを取得
        self.file_data.read_OSA_TXT()       # OSAのtxtファイルとして読み込み
        self.draw_graph()                   # 画面内に新しいグラフの描画

    # ファイルの選択
    def file_select(self):
        file = tk.filedialog.askopenfilename(title='ファイルを選択：OSA', filetypes=[('テキストファイル', 'txt'),('csvファイル', 'csv')])
        if not file:
            return
        self.file_data.set_file_data(file)
        self.file_data.read_OSA_TXT()
        self.draw_graph()
    
    def toggle_setting(self):
        if self.tgl_set_bln.get():
            self.commom_setting_frame['height'] = 78
            self.commom_setting_frame['width'] = 500

        else:
            self.commom_setting_frame['height'] = 1
            self.commom_setting_frame['width'] = 1


if __name__ == '__main__':
    win = TkinterDnD.Tk()
    app = GraphOSA(win)
    win.mainloop()
