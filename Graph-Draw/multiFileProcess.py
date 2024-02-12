import tkinter as tk
from decimal import *
from tkinter import Misc, scrolledtext, ttk, messagebox

from tkinterdnd2 import *

import sys
sys.path.append('./')

import graphAutocorrelation, graphESA, graphOSA, graphWaveform

class MultiFileConvert_win(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # 説明書き
        discription1 = ttk.Label(
            self.master,
            text='ドラッグ&ドロップでデータファイル追加。\nデータの種類をボタンで選択して[グラフ変換！]を押す。',
            font=("", 12),
            justify='center'
        )
        discription1.pack(pady=[15,0])

        # 説明書き2
        discription2 = ttk.Label(
            self.master,
            text='※R&S InstrumentViewを初期の場所にインストールしていれば、\nsetファイルからcsvを生成して描画します。',
            foreground='gray',
            font=("", 9),
            justify='center'
        )
        discription2.pack(pady=[5,0])

        # フレーム作成
        frame1 = ttk.Frame(self.master)

        # グラフ作成用のボタンをフレームに設置
        graph_button_frame = tk.Frame(frame1)
        self.OSAbutton = ttk.Button(graph_button_frame, default="active", text="OSA", width=15, padding=[0,7], command=self.make_OSA)
        self.WFbutton = ttk.Button(graph_button_frame, text="パルス波形", width=15, padding=[0,7], command=self.make_WF)
        self.ESAbutton = ttk.Button(graph_button_frame, text="ESA", width=15, padding=[0,7], command=self.make_ESA)
        self.ACbutton = ttk.Button(graph_button_frame, text="自己相関波形", width=15, padding=[0,7], command=self.make_AC)
        
        self.OSAbutton.grid(row=0, column=0, sticky=tk.EW)
        self.WFbutton.grid(row=0, column=1, sticky=tk.EW)
        self.ESAbutton.grid(row=1, column=0, sticky=tk.EW)
        self.ACbutton.grid(row=1, column=1, sticky=tk.EW)
        self.ACbutton.config()

        graph_button_frame.pack()
        frame1.pack()

        # どのグラフか選択
        self.garph_select = graphOSA.GraphOSA

        # フレーム
        frame2 = ttk.Frame(master=master)

        # グラフ作成ボタンを設置
        self.bulk_draw_button = ttk.Button(frame2, text="グラフ変換！", width=12, padding=[0,3], command=self.make_bulk_draph)
        self.bulk_draw_button.pack(side="left")

        # 読み込みリセット
        self.reset_file_list_button = ttk.Button(frame2, text="リセット", width=12, padding=[0,3], command=self.reset_file_list)
        self.reset_file_list_button.pack(side="left")

        # フレームパック
        frame2.pack(pady=5)

        # メッセージ
        class SingleMessage(tk.StringVar):
            def __init__(self, master: Misc | None = None, value: str | None = None, name: str | None = None) -> None:
                super().__init__(master, value, name)
                self.set_default()
            def set_default(self):
                self.set("読み込んだファイルを表示 パスに { と } は入れるな！")
        self.message = SingleMessage(self.master)
        self.message_label = ttk.Label(
            self.master,
            textvariable=self.message,
            font=("", 10),
            justify='center'
            )
        self.message_label.pack()
        self.message_label.propagate(False)

        # スクロールバー付きのテキストウィジェットを作成
        self.loaded_file_list_area = scrolledtext.ScrolledText(master=master, wrap=tk.WORD, width=40, height=10)
        self.loaded_file_list_area.pack(padx=10, pady=(0, 10), fill=tk.BOTH, expand=True)

        # ドラック＆ドロップ導入
        self.master.drop_target_register(DND_FILES)
        self.master.dnd_bind("<<Drop>>", self.get_dnd_file_path)

        # ファイルパス
        self.loaded_file_path_list = []

    def get_dnd_file_path(self, event: TkinterDnD.DnDEvent):
        next_file = ""
        in_bracket = False
        for c in event.data:
            if c == "{":
                in_bracket = True
                continue
            elif in_bracket:
                if c == "}":
                    in_bracket = False
                    self.loaded_file_path_list.append(next_file)
                    next_file = ""
                    continue
            elif c == " ":
                if next_file != "":
                    self.loaded_file_path_list.append(next_file)
                    next_file = ""
                continue
            
            next_file += c
        
        self.reload_loaded_file_list_area()

    def reload_loaded_file_list_area(self):
        new_text = ""
        for line in self.loaded_file_path_list:
            new_text += line + "\n"
        new_text = new_text.strip()
        
        self.loaded_file_list_area.delete(1.0, tk.END)
        self.loaded_file_list_area.insert(tk.INSERT, new_text)
        self.message.set_default()

    def make_bulk_draph(self):
        if self.loaded_file_path_list == []:
            return

        sub_win = tk.Toplevel(self.master)
        sub_win.title('temp')
        graph = self.garph_select(sub_win)

        for file_path in self.loaded_file_path_list:
            graph.file_data.set_file_data(file_path)

            if self.garph_select == graphOSA.GraphOSA:
                graph.file_data.read_OSA_TXT()
            elif self.garph_select == graphWaveform.GraphWaveform:
                graph.file_data.read_oscillo_csv()
            elif self.garph_select == graphESA.GraphESA:
                graph.file_data.read_ESA()
            elif self.garph_select == graphAutocorrelation.GraphAutocorrelation:
                graph.file_data.read_oscillo_csv()
            
            graph.draw_graph()
            graph.toolbar.force_save_figure()
        
        sub_win.destroy()
        self.message.set("変換完了！！")

    def reset_file_list(self):
        self.loaded_file_path_list = []
        self.reload_loaded_file_list_area()
        self.message.set_default()

    def make_OSA(self):
        self.OSAbutton.config(default="active")
        self.WFbutton.config(default="normal")
        self.ESAbutton.config(default="normal")
        self.ACbutton.config(default="normal")
        self.garph_select = graphOSA.GraphOSA

    def make_WF(self):
        self.OSAbutton.config(default="normal")
        self.WFbutton.config(default="active")
        self.ESAbutton.config(default="normal")
        self.ACbutton.config(default="normal")
        self.garph_select = graphWaveform.GraphWaveform

    def make_ESA(self):
        self.OSAbutton.config(default="normal")
        self.WFbutton.config(default="normal")
        self.ESAbutton.config(default="active")
        self.ACbutton.config(default="normal")
        self.garph_select = graphESA.GraphESA

    def make_AC(self):
        self.OSAbutton.config(default="normal")
        self.WFbutton.config(default="normal")
        self.ESAbutton.config(default="normal")
        self.ACbutton.config(default="active")
        self.garph_select = graphAutocorrelation.GraphAutocorrelation

if __name__ == '__main__':
    #ウィンドウ作製    
    main_win = TkinterDnD.Tk()
    win_w = 500
    win_h = 380
    sw = main_win.winfo_screenwidth()
    sh = main_win.winfo_screenheight()
    main_win.geometry(str(win_w) + 'x' + str(win_h) + '+' + str(int(sw/2-win_w/2)) + '+' + str(int(sh/2-win_h/2)))
    main_win.title("グラフ画像の一括生成")

    app = MultiFileConvert_win(main_win)
    main_win.mainloop()
