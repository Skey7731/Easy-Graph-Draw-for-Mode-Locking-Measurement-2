# GraphAutocorrelation.py

import tkinter as tk
from tkinter import ttk

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

class GraphAutocorrelation(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        #-----------------------------------------------
        # データ保存用
        self.file_data = fileData.FileData(['csv'])

        self.x = []
        self.y = []

        # パルス幅表示と近似波形の選択
        self.AC_width = None    # 自己相関幅
        self.FWHM_text = tk.StringVar()
        self.FWHM_text.set('-ファイル名-\nパルス幅： 0 ps 換算スペクトル幅: 0 nm')
        FWHM_label = tk.Label(self.master, textvariable=self.FWHM_text)

        rd_frame = tk.Frame(self.master)
        self.rd_state = tk.IntVar()
        self.rd_state.set(1)
        rd_button1 = ttk.Radiobutton(rd_frame, variable=self.rd_state, value='1', text='sech²', command=self.calc_pulse_width)
        rd_button2 = ttk.Radiobutton(rd_frame, variable=self.rd_state, value='2', text='ガウシアン', command=self.calc_pulse_width)

        # これの配置
        FWHM_label.pack()
        rd_button1.pack(side='left')
        rd_button2.pack(side='left')
        rd_frame.pack()

        # 縦軸のCH選択
        CH_frame = tk.Frame(self.master)
        self.CH_state = tk.IntVar()
        self.CH_state.set(1)
        self.CH_button1 = ttk.Radiobutton(CH_frame, variable=self.CH_state, value='1', text='CH1', command=self.draw_graph)
        self.CH_button2 = ttk.Radiobutton(CH_frame, variable=self.CH_state, value='2', text='CH2', command=self.draw_graph)

        # 縦軸の正規化
        self.normalize_y_state = tk.BooleanVar()
        self.normalize_y_button = tk.Checkbutton(CH_frame, variable=self.normalize_y_state, text='y軸を正規化', command=self.draw_graph)

        # これの配置
        self.CH_button1.pack(side='left')
        self.CH_button2.pack(side='left')
        self.normalize_y_button.pack(side='left', padx=[10,0])
        CH_frame.pack()

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

        #グラフタイトル設定
        self.ax.set_title('Autocorrelation Waveform', fontsize=22, visible=True)
        
        #軸ラベル設定
        self.ax.set_xlabel('Delay time / ps', visible=True)
        self.ax.set_ylabel('Intensity / V', visible=True)

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

        # 縦軸のチャンネルの選択
        if self.file_data.y1 and (not self.file_data.y2):
            self.CH_state.set(1)
            self.CH_button1['state'] = 'abled'
            self.CH_button2['state'] = 'disabled'
        elif self.file_data.y2 and (not self.file_data.y1):
            self.CH_state.set(2)
            self.CH_button1['state'] = 'disabled'
            self.CH_button2['state'] = 'abled'
        else:
            self.CH_button1['state'] = 'abled'
            self.CH_button2['state'] = 'abled'

        # xの設定
        self.x = [i * 1e3 * 15.5 for i in self.file_data.x]
        # yの設定
        if self.CH_state.get() == 1:
            self.y = self.file_data.y1
        else:
            self.y = self.file_data.y2
        # ピークの位置をτ=0に
        center = self.y.index(max(self.y))
        center_x = self.x[center]
        self.x = [i - center_x for i in self.x]
        # 正規化
        if self.normalize_y_state.get():
            self.ax.set_ylabel('Normalized Intensity / a.u.', visible=True)
            y_max = max(self.y)
            self.y = [i / y_max for i in self.y]
        else:
            self.ax.set_ylabel('Intensity / V', visible=True)

        # プロット
        self.ax.plot(self.x, self.y)

        # 各種設定の反映
        self.settings.init_settings()
        self.settings.apply_settings()

        # パルス幅の計算
        plot_li =[]
        for i in range(len(self.x)):
            plot_li.append([self.x[i], self.y[i]])

        FWHM = usefulModules.calc_FWHM(plot_li, 'mW', 3)
        if FWHM[1]:
            self.AC_width = FWHM[0]
            self.calc_pulse_width()
        else:
            self.FWHM_text.set(self.file_data.file_name + '\nパルス幅: error 換算スペクトル幅: 0 nm')
        
        # ウィンドウタイトルの設定
        self.master.title('AC ' + self.file_data.file_path)

    def calc_pulse_width(self):
        # 半値幅が計算できてない場合return
        if not self.AC_width:
            self.FWHM_text.set(self.file_data.file_name + '\nパルス幅: error 換算スペクトル幅: 0 nm')
            return
        
        if self.rd_state.get() == 1:
            pulse_width = self.AC_width / 1.54  # sech²
            conv_spectrum_w = 2.52 / pulse_width
        elif self.rd_state.get() == 2:
            pulse_width = self.AC_width / 1.41  # ガウシアン
            conv_spectrum_w = 3.53 / pulse_width
        pulse_width = round(pulse_width, 2)
        
        self.FWHM_text.set(self.file_data.file_name + '\nパルス幅: {} ps 換算スペクトル幅: {} nm'.format(pulse_width, round(conv_spectrum_w, 3)))

    # ファイルドロップ時の処理
    def process_droped_file(self, event):
        self.file_data.dnd_get_path(event)  # ファイルの名前やパスを取得
        self.file_data.read_oscillo_csv()   # 自己相関のcsvファイルとして読み込み
        self.draw_graph()                   # 画面内に新しいグラフの描画

    # ファイルの選択
    def file_select(self):
        file = tk.filedialog.askopenfilename(title='ファイルを選択：自己相関波形', filetypes=[('csvファイル', 'csv')])
        if not file:
            return
        self.file_data.set_file_data(file)
        self.file_data.read_oscillo_csv()
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
    app = GraphAutocorrelation(win)
    win.mainloop()
