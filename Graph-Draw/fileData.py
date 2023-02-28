# fileData.py

import csv
import os
import re
import subprocess
from tkinter import messagebox

class FileData:
    def __init__(self, exs:list):
        self.folder_path = ''
        self.file_path = ''
        self.file_name = ''
        self.file_ex = ''
        self.allow_ex = exs

        self.x =[]
        self.y1 = []
        self.y2 = []

    def failed_reading(self):
        messagebox.showerror('Read error','ファイルデータの読み取りに失敗しました。')
        # グラフをばってんに
        self.x = [-1, 1, 0, -1, 1]
        self.y1 = [-1, 1, 0, 1, -1]
        self.y2 = []

    def dnd_path_shaping(self, s):
        if s[0] == "{":
            s = s[1:len(s)-1]
        return s

    def dnd_get_path(self, event):
        # {}の除去
        file = self.dnd_path_shaping(event.data)

        # ファイルの存在確認
        if os.path.isfile(file) == False:
            messagebox.showerror('Path error',"複数ファイル、またはフォルダーを選択はできません。")
            return

        # 拡張子の確認
        fol = re.search(r'.*/', file)
        temp_folder_path = fol.group()
        s, e = fol.span()
        temp_file_name = file[e:]
        ex = re.search(r'.*\.', file)
        s, e = ex.span()
        ex = file[e:]
        if ex not in self.allow_ex:
            messagebox.showerror('Extension error',"拡張子を確認してください。\n取得ファイル -> {}\n読み込み可能な拡張子 -> {}".format(temp_file_name, self.allow_ex))
            return

        #変数にファイルデータ代入
        self.file_path = file
        fol = re.search(r'.*/', file)
        self.folder_path = fol.group()
        s, e = fol.span()
        self.file_name = file[e:]
        ex = re.search(r'.*\.', file)
        s, e = ex.span()
        self.file_ex = file[e:]

    def set_file_data(self, file):
        #変数にファイルデータ代入
        self.file_path = file
        fol = re.search(r'.*/', file)
        self.folder_path = fol.group()
        s, e = fol.span()
        self.file_name = file[e:]
        ex = re.search(r'.*\.', file)
        s, e = ex.span()
        self.file_ex = file[e:]

    def read_oscillo_csv(self):
        try:
            with open(self.file_path) as f:
                reader = list(csv.reader(f))
            
            # Increment の取得
            increment_column = reader[0].index('Increment')
            increment = float(reader[1][increment_column])
            
            # CH1 の取得
            if 'CH1' in reader[0]:
                CH1_column = reader[0].index('CH1')
                self.y1 = [float(i[CH1_column]) for i in reader[2:]]
            else:
                self.y1 = []

            # CH2 の取得
            if 'CH2' in reader[0]:
                CH2_column = reader[0].index('CH2')
                self.y2 = [float(i[CH2_column]) for i in reader[2:]]
            else:
                self.y2 = []

            # 横軸データの生成
            self.x = [i * increment for i in range(max(len(self.y1), len(self.y2)))]

        except:
            self.failed_reading()
            return

    def read_OSA_TXT(self):
        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                reader = list(csv.reader(f))
            for i in reader:
                if len(i)==0:
                    continue
                if i[0] == 'SMPL':
                    smpl = int(i[1])
                    break
            
            # 中身のリセット
            self.x = []
            self.y1 = []
            
            # データ点の追加
            for i in range(3, 3+smpl):
                self.x.append(float(reader[i][0]))
                self.y1.append(float(reader[i][1]))

        except:
            self.failed_reading()
            return

    def read_ESA(self):
        # setファイルはcsvに変換して保存
        try:
            if self.file_ex == 'set':
                file = repr(self.file_path)[1:-1]
                newfile = repr(self.file_path)[1:-4] + r'csv'
                
                # ファイルが既にあった場合の確認
                if os.path.isfile(newfile):
                    rep =  messagebox.askyesno('確認', 'csvファイルが既に存在します。-> {}\nそのまま用いますか？'.format(self.file_name[:-3] + 'csv'))
                    if rep:
                        self.file_path = newfile
                        self.file_name = self.file_name[:-3] + 'csv'
                        self.file_ex = 'csv'
                    else:
                        rep = messagebox.askyesno('確認', '上書きしてもよろしいですか？')
                        if rep:
                            # ファイルの変換
                            command = 'InstrumentView.exe -ConvertToCSV "{}" "{}"'.format(file, newfile)
                            subprocess.run(command, shell=True, capture_output=True, text=True, cwd='C:/Program Files (x86)/Rohde-Schwarz/InstrumentView/')
                            self.file_path = newfile
                            self.file_name = self.file_name[:-3] + 'csv'
                            self.file_ex = 'csv'
                        else:
                            return
                else:
                    # ファイルの変換
                    command = 'InstrumentView.exe -ConvertToCSV "{}" "{}"'.format(file, newfile)
                    subprocess.run(command, shell=True, capture_output=True, text=True, cwd='C:/Program Files (x86)/Rohde-Schwarz/InstrumentView/')
                    self.file_path = newfile
                    self.file_name = self.file_name[:-3] + 'csv'
                    self.file_ex = 'csv'

        except:
            messagebox.showerror('Error','ファイルの変換に失敗しました。')
            # グラフをばってんに
            self.x = [-1, 1, 0, -1, 1]
            self.y1 = [-1, 1, 0, 1, -1]
            self.y2 = []
            return
        
        # csvの読み取り
        try:
            with open(self.file_path, encoding="utf-8") as f:
                reader = list(csv.reader(f))
            for i, j in enumerate(reader):
                if len(j) == 0:
                    continue
                if j[0] == 'Frequency [Hz]':
                    start_index = i+1
                    break
            
            # 中身のリセット
            self.x = []
            self.y1 = []
            self.y2 = []
            
            # データ点の追加
            if not reader[start_index-1][2]:
                self.x = [float(i[0]) for i in reader[start_index:]]
                self.y1 = [float(i[1]) for i in reader[start_index:]]

            elif not reader[start_index-1][3]:
                self.x = [float(i[0]) for i in reader[start_index:]]
                self.y1 = [float(i[1]) for i in reader[start_index:]]
                self.y2 = [float(i[2]) for i in reader[start_index:]]

        except:
            self.failed_reading()
            return

