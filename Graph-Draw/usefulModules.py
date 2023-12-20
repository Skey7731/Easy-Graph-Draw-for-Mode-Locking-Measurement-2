# usefulModules.py

import matplotlib as mpl
import os
import tkinter
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

# リストからFWHMの計算
def calc_FWHM(plot_li:list, unit:str, round_digit:int):
    # plot_li format >> list of [Index, Intnsity]

    intensity = [i[1] for i in plot_li]
    max_value = max(intensity)
    max_pos = intensity.index(max_value)
    if unit == 'dB':
        half_I = max_value - 3
    elif unit == 'mW':
        half_I = max_value / 2
    else:
        half_I = None

    L_FWHM = max_value
    R_FWHM = max_value
    L_index = max_pos
    R_index = max_pos

    #左右方向で半分以下の強度になる一点手前を探索
    err = False
    try:
        while True:
            if intensity[L_index-1] < half_I:
                break
            L_index = L_index -1
            L_FWHM = intensity[L_index]
    except IndexError:
        L_FWHM = intensity[0]
        err = True
        
    try:
        while True:
            if intensity[R_index+1] < half_I:
                break
            R_index = R_index +1
            R_FWHM = intensity[R_index]
    except IndexError:
        R_FWHM = intensity[-1]
        err = True

    if err:
        FWHM = [round(float(plot_li[R_index][0]) - float(plot_li[L_index][0]), round_digit), False]
        return FWHM
    else:
        FWHM = [round(float(plot_li[R_index][0]) - float(plot_li[L_index][0]), round_digit), True]
        return FWHM

# NavigationToolbar2Tk.save_figureのオーバーライド
# ファイル名と初期ディレクトリをグラフに読み込んだファイルの物に変更
class my_NavigationToolbar2Tk(NavigationToolbar2Tk):
    def __init__(self, file_data, canvas, window=None):
        super().__init__(canvas, window)

        # FileDataインスタンスの受け取り
        self.file_data = file_data

        # ファイル名の保持
        self.file_name = None

    def save_figure(self, *args):
        filetypes = self.canvas.get_supported_filetypes().copy()
        default_filetype = self.canvas.get_default_filetype()

        # Tk doesn't provide a way to choose a default filetype,
        # so we just have to put it first
        default_filetype_name = filetypes.pop(default_filetype)
        sorted_filetypes = ([(default_filetype, default_filetype_name)]
                            + sorted(filetypes.items()))
        tk_filetypes = [(name, '*.%s' % ext) for ext, name in sorted_filetypes]

        # adding a default extension seems to break the
        # asksaveasfilename dialog when you choose various save types
        # from the dropdown.  Passing in the empty string seems to
        # work - JDH!
        # defaultextension = self.canvas.get_default_filetype()
        defaultextension = ''
        initialdir = self.file_data.folder_path   # os.path.expanduser(mpl.rcParams['savefig.directory'])
        initialfile = self.file_data.file_name[:-4] if self.file_name is None else self.file_name   # self.canvas.get_default_filename()
        fname = tkinter.filedialog.asksaveasfilename(
            master=self.canvas.get_tk_widget().master,
            title='Save the figure',
            filetypes=tk_filetypes,
            defaultextension=defaultextension,
            initialdir=initialdir,
            initialfile=initialfile,
            )

        if fname in ["", ()]:
            return
        # Save dir for next time, unless empty str (i.e., use cwd).
        if initialdir != "":
            mpl.rcParams['savefig.directory'] = (
                os.path.dirname(str(fname)))
        try:
            # This method will handle the delegation to the correct type
            self.canvas.figure.savefig(fname)
        except Exception as e:
            tkinter.messagebox.showerror("Error saving file", str(e))