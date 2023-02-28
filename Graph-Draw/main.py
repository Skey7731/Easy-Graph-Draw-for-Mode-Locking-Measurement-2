import os
import tkinter as tk
from decimal import *
from tkinter import filedialog, ttk

from tkinterdnd2 import *

import sys
sys.path.append('./')

import fileData, graphAutocorrelation, graphESA, graphOSA, graphWaveform

class Main(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # 著作権表示
        license_label = ttk.Label(
            self.master,
            foreground='gray',
            text='Copyright © 2001-2022 Python Software Foundation; All Rights Reserved',
            font=("Arial Narrow", 10)
            )
        license_label.pack(anchor=tk.W)
        
        # 説明書き
        discription1 = ttk.Label(
            self.master,
            text='ボタンを押すとグラフ用の新しいウィンドウが生成されます。\nそれぞれのウィンドウにファイルをドロップすることで再描画が可能です。',
            font=("", 12),
            justify='center'
        )
        discription1.pack(pady=[15,0])

        # 説明書き2
        discription2 = ttk.Label(
            self.master,
            text='※R&S InstrumentViewを初期の場所にインストールしていれば、setファイルからcsvを生成して描画します。\n※ファイル選択時、右下のプルダウンから拡張子を選択できます。',
            foreground='gray',
            font=("", 9),
            justify='center'
        )
        discription2.pack(pady=[5,0])

        # ファイル選択チェックボタン
        self.select_bln = tk.BooleanVar(value=False)
        select_file = ttk.Checkbutton(
            self.master,
            text='ウィンドウを開く際にファイルを選択',
            variable=self.select_bln,
        )
        select_file.pack(pady=[15,0])

        # フレーム作成
        frame1 = ttk.Frame(self.master)

        # グラフ作成用のボタンをフレームに設置
        graph_button_frame = tk.Frame(frame1)
        OSAbutton = ttk.Button(graph_button_frame, text="OSAグラフの表示", width=18, padding=[0,10], command=self.make_OSA)
        WFbutton = ttk.Button(graph_button_frame, text="パルス波形の表示", width=18, padding=[0,10], command=self.make_WF)
        ESAbutton = ttk.Button(graph_button_frame, text="ESAグラフの表示", width=18, padding=[0,10], command=self.make_ESA)
        ACbutton = ttk.Button(graph_button_frame, text="自己相関波形の表示", width=18, padding=[0,10], command=self.make_AC)
        
        OSAbutton.grid(row=0, column=0, sticky=tk.EW)
        WFbutton.grid(row=0, column=1, sticky=tk.EW)
        ESAbutton.grid(row=1, column=0, sticky=tk.EW)
        ACbutton.grid(row=1, column=1, sticky=tk.EW)
        
        graph_button_frame.pack()
        frame1.pack()

    def make_OSA(self):
        sub_win = tk.Toplevel(self.master)
        sub_win.title('OSA')
        graph = graphOSA.GraphOSA(sub_win)

        if self.select_bln.get():
            file = filedialog.askopenfilename(title='ファイルを選択：OSA', filetypes=[('テキストファイル', 'txt'),('csvファイル', 'csv')])
            if not file:
                return
            graph.file_data.set_file_data(file)
            graph.file_data.read_OSA_TXT()

        graph.draw_graph()

    def make_WF(self):
        sub_win = tk.Toplevel(self.master)
        sub_win.title('Waveform')
        graph = graphWaveform.GraphWaveform(sub_win)

        if self.select_bln.get():
            file = filedialog.askopenfilename(title='ファイルを選択：パルス波形', filetypes=[('csvファイル', 'csv')])
            if not file:
                return
            graph.file_data.set_file_data(file)
            graph.file_data.read_oscillo_csv()

        graph.draw_graph()

    def make_ESA(self):
        sub_win = tk.Toplevel(self.master)
        sub_win.title('ESA')
        graph = graphESA.GraphESA(sub_win)

        if self.select_bln.get():
            file = filedialog.askopenfilename(title='ファイルを選択：ESA', filetypes=[('csvファイル', 'csv'),('setファイル', 'set')])
            if not file:
                return
            graph.file_data.set_file_data(file)
            graph.file_data.read_ESA()

        graph.draw_graph()

    def make_AC(self):
        sub_win = tk.Toplevel(self.master)
        sub_win.title('Autocorrelation')
        graph = graphAutocorrelation.GraphAutocorrelation(sub_win)

        if self.select_bln.get():
            file = filedialog.askopenfilename(title='ファイルを選択：自己相関波形', filetypes=[('csv', 'csv')])
            if not file:
                return
            graph.file_data.set_file_data(file)
            graph.file_data.read_oscillo_csv()

        graph.draw_graph()

if __name__ == '__main__':
    #ウィンドウ作製    
    main_win = TkinterDnD.Tk()
    win_w = 600
    win_h = 260
    sw = main_win.winfo_screenwidth()
    sh = main_win.winfo_screenheight()
    main_win.geometry(str(win_w) + 'x' + str(win_h) + '+' + str(int(sw/2-win_w/2)) + '+' + str(int(sh/2-win_h/2)))
    main_win.title("データ→グラフ変換ソフト v1.0.2")

    app = Main(main_win)
    main_win.mainloop()
