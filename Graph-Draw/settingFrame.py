# settingFrame.py
import copy
import tkinter as tk
from tkinter import ttk, simpledialog

# グラフと一緒に設置して調整を行う。設置先グラフであらかじめプロットは行い、x,yとグラフタイトル、軸ラベルも先に設定する必要あり。
class SettingFrame(tk.Frame):
    def __init__(self, graph_frame, master=None):
        super().__init__(master)
        self.master = master
        self.graph_frame = graph_frame

        # グラフにプロットするx,y
        self.graph_x = []
        self.graph_y = []

        # グラフタイトル
        self.graph_title = 'Sample Title'

        # 軸ラベル
        self.x_label = 'X Label'
        self.y_label = 'Y Label'

        # 調整ウィジェットをフレームにまとめて設置　x軸範囲、y軸範囲、その他

        #--XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX--
        # フレーム
        setting_frame_xlim = tk.Frame(self.master)
        
        # x軸範囲ボタン説明
        self.xlim_text = ttk.Label(setting_frame_xlim, text='X軸範囲を設定')

        self.xlim_text.pack(side=tk.LEFT)

        # x軸範囲ボタン
        self.x_min_btn_txt = tk.StringVar()
        self.x_max_btn_txt = tk.StringVar()
        self.x_min_btn_txt.set('0.0')
        self.x_max_btn_txt.set('1.0')
        self.x_min_btn = ttk.Button(setting_frame_xlim, textvariable=self.x_min_btn_txt, command = self.x_min_ask)
        self.x_max_btn = ttk.Button(setting_frame_xlim, textvariable=self.x_max_btn_txt, command = self.x_max_ask)
        
        self.x_min_btn.pack(side=tk.LEFT)
        self.x_max_btn.pack(side=tk.LEFT)

        # x軸範囲fixチェックボタン
        self.xlim_fix_bln = tk.BooleanVar()
        self.xlim_fix_bln.set(False)
        xlim_fixbtn = tk.Checkbutton(setting_frame_xlim, variable=self.xlim_fix_bln, text='固定', command=self.apply_settings)

        xlim_fixbtn.pack(side=tk.LEFT)

        # リセットボタン
        self.x_lim_reset_button = ttk.Button(setting_frame_xlim, text='リセット', command=self.x_reset)
        self.x_lim_reset_button.pack(side=tk.LEFT)

        # フレーム設置
        setting_frame_xlim.pack(expand=True, anchor=tk.CENTER)
        #--XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX--

        #--YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY--
        # フレーム
        setting_frame_ylim = tk.Frame(self.master)

        # y軸範囲ボタン説明
        self.ylim_text = ttk.Label(setting_frame_ylim, text='Y軸範囲を設定')

        self.ylim_text.pack(side=tk.LEFT)

        # y軸範囲ボタン
        self.y_min_btn_txt = tk.StringVar()
        self.y_max_btn_txt = tk.StringVar()
        self.y_min_btn_txt.set('0.0')
        self.y_max_btn_txt.set('1.0')
        self.y_min_btn = ttk.Button(setting_frame_ylim, textvariable=self.y_min_btn_txt, command = self.y_min_ask)
        self.y_max_btn = ttk.Button(setting_frame_ylim, textvariable=self.y_max_btn_txt, command = self.y_max_ask)
        
        self.y_min_btn.pack(side=tk.LEFT)
        self.y_max_btn.pack(side=tk.LEFT)

        # y軸範囲fixチェックボタン
        self.ylim_fix_bln = tk.BooleanVar()
        self.ylim_fix_bln.set(False)
        ylim_fixbtn = tk.Checkbutton(setting_frame_ylim, variable=self.ylim_fix_bln, text='固定', command=self.apply_settings)

        ylim_fixbtn.pack(side=tk.LEFT)

        # リセットボタン
        self.y_lim_reset_button = ttk.Button(setting_frame_ylim, text='リセット', command=self.y_reset, padding=[0,0])
        self.y_lim_reset_button.pack(side=tk.LEFT)

        # フレーム設置
        setting_frame_ylim.pack(expand=True, anchor=tk.CENTER)
        #--YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY--

        
        #--OTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERs--
        # フレーム
        setting_frame_others = tk.Frame(self.master)

        #タイトル、軸ラベル、グリッド線設定用フレーム
        b_Lframe = tk.Frame(setting_frame_others)
        # タイトルのありなし
        self.graph_title_bln = tk.BooleanVar()
        self.graph_title_bln.set(True)
        isgraphtitle = tk.Checkbutton(b_Lframe, text='グラフタイトル', variable=self.graph_title_bln, command=self.apply_settings)
        isgraphtitle.pack(side=tk.RIGHT)

        # 軸ラベルのありなし
        self.axe_label_bln = tk.BooleanVar()
        self.axe_label_bln.set(True)
        isaxelabel = tk.Checkbutton(b_Lframe, text='軸ラベル', variable=self.axe_label_bln, command=self.apply_settings)
        isaxelabel.pack(side=tk.RIGHT)
        
        # グリッド線のありなし
        self.grid_bln = tk.BooleanVar()
        self.grid_bln.set(True)
        isgrid = tk.Checkbutton(b_Lframe, text='グリッド線', variable=self.grid_bln, command=self.apply_settings)
        isgrid.pack(side=tk.RIGHT)

        # 色ボタン用フレーム
        b_Rframe = tk.Frame(setting_frame_others)
        # プロット色ボタン
        label = tk.Label(b_Rframe, text='プロット色')
        self.plt_color = 'black'

        self.button0 = tk.Button(b_Rframe, height=0, width=3, bg='black', activebackground='black', command=self.b0, relief=tk.SUNKEN)
        self.button1 = tk.Button(b_Rframe, height=0, width=3, bg='#4472c4', activebackground='#4472c4', command=self.b1)
        self.button2 = tk.Button(b_Rframe, height=0, width=3, bg='#ed7d31', activebackground='#ed7d31', command=self.b2)
        self.button3 = tk.Button(b_Rframe, height=0, width=3, bg='#ffc000', activebackground='#ffc000', command=self.b3)
        self.button4 = tk.Button(b_Rframe, height=0, width=3, bg='#70ad47', activebackground='#70ad47', command=self.b4)

        label.pack(side=tk.LEFT)
        self.button0.pack(side=tk.LEFT)
        self.button1.pack(side=tk.LEFT)
        self.button2.pack(side=tk.LEFT)
        self.button3.pack(side=tk.LEFT)
        self.button4.pack(side=tk.LEFT)

        # 2段目中身のフレーム設置
        b_Lframe.pack(expand=True, fill=tk.BOTH, side=tk.LEFT, anchor=tk.W)
        b_Rframe.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT, anchor=tk.E)

        # フレーム2段目設置
        setting_frame_others.pack(expand=True, fill=tk.BOTH)
        #--OTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERsOTHERs--

    # x軸の最大値最小値設定
    def x_min_ask(self):
        s = simpledialog.askfloat('入力', 'x軸の最小値を入力')
        if s == None:
            return
        self.x_min_btn_txt.set(str(s))
        self.apply_settings()

    def x_max_ask(self):
        s = simpledialog.askfloat('入力', 'x軸の最大値を入力')
        if s == None:
            return
        self.x_max_btn_txt.set(str(s))
        self.apply_settings()
    
    # x範囲のリセット
    def x_reset(self):
        temp_y_lim = copy.copy(self.graph_frame.ax.get_ylim())
        self.graph_frame.draw_graph()
        self.y_min_btn_txt.set(str(temp_y_lim[0]))
        self.y_max_btn_txt.set(str(temp_y_lim[1]))
        self.apply_settings()

    # y軸の最大値最小値設定
    def y_min_ask(self):
        s = simpledialog.askfloat('入力', 'y軸の最小値を入力')
        if s == None:
            return
        self.y_min_btn_txt.set(str(s))
        self.apply_settings()

    def y_max_ask(self):
        s = simpledialog.askfloat('入力', 'y軸の最大値を入力')
        if s == None:
            return
        self.y_max_btn_txt.set(str(s))
        self.apply_settings()
    
    # y範囲のリセット
    def y_reset(self):
        temp_x_lim = copy.copy(self.graph_frame.ax.get_xlim())
        self.graph_frame.draw_graph()
        self.x_min_btn_txt.set(str(temp_x_lim[0]))
        self.x_max_btn_txt.set(str(temp_x_lim[1]))
        self.apply_settings()

    # プロット色ボタン動作
    def b0(self):
        self.button0.config(relief=tk.SUNKEN)
        self.button1.config(relief=tk.RAISED)
        self.button2.config(relief=tk.RAISED)
        self.button3.config(relief=tk.RAISED)
        self.button4.config(relief=tk.RAISED)
        self.plt_color = 'black'
        self.apply_settings()
        
    def b1(self):
        self.button0.config(relief=tk.RAISED)
        self.button1.config(relief=tk.SUNKEN)
        self.button2.config(relief=tk.RAISED)
        self.button3.config(relief=tk.RAISED)
        self.button4.config(relief=tk.RAISED)
        self.plt_color = '#4472c4'
        self.apply_settings()
        
    def b2(self):
        self.button0.config(relief=tk.RAISED)
        self.button1.config(relief=tk.RAISED)
        self.button2.config(relief=tk.SUNKEN)
        self.button3.config(relief=tk.RAISED)
        self.button4.config(relief=tk.RAISED)
        self.plt_color = '#ed7d31'
        self.apply_settings()
        
    def b3(self):
        self.button0.config(relief=tk.RAISED)
        self.button1.config(relief=tk.RAISED)
        self.button2.config(relief=tk.RAISED)
        self.button3.config(relief=tk.SUNKEN)
        self.button4.config(relief=tk.RAISED)
        self.plt_color = '#ffc000'
        self.apply_settings()

    def b4(self):
        self.button0.config(relief=tk.RAISED)
        self.button1.config(relief=tk.RAISED)
        self.button2.config(relief=tk.RAISED)
        self.button3.config(relief=tk.RAISED)
        self.button4.config(relief=tk.SUNKEN)
        self.plt_color = '#70ad47'
        self.apply_settings()

    def init_settings(self):
        # グラフにプロットするx,yを取得
        self.graph_x = self.graph_frame.x
        self.graph_y = self.graph_frame.y

        # グラフタイトルを取得
        if self.graph_title_bln.get():
            self.graph_title = self.graph_frame.ax.get_title()

        # 軸ラベルを取得
        if self.axe_label_bln.get():
            self.x_label = self.graph_frame.ax.get_xlabel()
            self.y_label = self.graph_frame.ax.get_ylabel()

        # 軸の範囲設定
        if self.xlim_fix_bln.get() == False:
            self.graph_frame.ax.set_xlim(self.graph_x[0], self.graph_x[-1])
            self.x_min_btn_txt.set(str(self.graph_x[0]))
            self.x_max_btn_txt.set(str(self.graph_x[-1]))

        if self.ylim_fix_bln.get() == False:
            band = max(self.graph_y) - min(self.graph_y)
            self.graph_frame.ax.set_ylim(min(self.graph_y) - band/5, max(self.graph_y) + band/5)
            self.y_min_btn_txt.set(str(min(self.graph_y) - band/5))
            self.y_max_btn_txt.set(str(max(self.graph_y) + band/5))

    def apply_settings(self):
        # まずプロットを除去
        if self.graph_frame.ax.lines:
            self.graph_frame.ax.lines[0].remove()
        else:
            return  # プロットがない場合何もしない

        # x軸の範囲
        if self.xlim_fix_bln.get() == False:
            self.x_min_btn['state'] = 'abled'
            self.x_max_btn['state'] = 'abled'
            self.x_lim_reset_button['state'] = 'abled'
            self.graph_frame.ax.set_xlim(float(self.x_min_btn_txt.get()), float(self.x_max_btn_txt.get()))
        else:
            self.x_min_btn['state'] = 'disabled'
            self.x_max_btn['state'] = 'disabled'
            self.x_lim_reset_button['state'] = 'disabled'
            self.graph_frame.ax.set_xlim(float(self.x_min_btn_txt.get()), float(self.x_max_btn_txt.get()))
        
        # y軸の範囲
        if self.ylim_fix_bln.get() == False:
            self.y_min_btn['state'] = 'abled'
            self.y_max_btn['state'] = 'abled'
            self.y_lim_reset_button['state'] = 'abled'
            self.graph_frame.ax.set_ylim(float(self.y_min_btn_txt.get()), float(self.y_max_btn_txt.get()))
        else:
            self.y_min_btn['state'] = 'disabled'
            self.y_max_btn['state'] = 'disabled'
            self.y_lim_reset_button['state'] = 'disabled'
            self.graph_frame.ax.set_ylim(float(self.y_min_btn_txt.get()), float(self.y_max_btn_txt.get()))

        
        # グラフタイトル設定
        if self.graph_title_bln.get():
            self.graph_frame.ax.set_title(self.graph_title, fontsize=22, visible=True)
        else:
            self.graph_frame.ax.set_title(self.graph_title, fontsize=22, visible=False)
        
        # 軸ラベル設定
        if self.axe_label_bln.get():
            self.graph_frame.ax.set_xlabel(self.x_label , fontsize=22, visible=True)
            self.graph_frame.ax.set_ylabel(self.y_label, fontsize=22, visible=True)
        else:
            self.graph_frame.ax.set_xlabel(self.x_label , fontsize=22, visible=False)
            self.graph_frame.ax.set_ylabel(self.y_label, fontsize=22, visible=False)

        # グリッド線設定
        if self.grid_bln.get():
            self.graph_frame.ax.grid(
                color='gray',
                alpha=0.5)
            self.graph_frame.ax.grid(True)
        else:
            self.graph_frame.ax.grid(False)

        #グラフの描画
        self.graph_frame.ax.plot(self.graph_x, self.graph_y, color=self.plt_color)
        self.graph_frame.fig_canvas.draw()
