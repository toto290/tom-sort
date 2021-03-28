import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import os
import datetime
from pathlib import Path
from PIL import Image, ImageTk
import Styles
import sqlite3


class TomSort(tk.Tk):
    def __init__(self, title):
        tk.Tk.__init__(self)

        # Settings
        self.valid_photo_types = ['.jpg', '.JPG', '.png', '.PNG']

        # Paths
        self.root_path = os.path.dirname(__file__)
        self.media_path = Path.joinpath(Path(self.root_path), 'images')

        # Initial parameters
        self.mode = tk.IntVar()
        self.mode.set(1)    # start:0 sort:1 twin:2
        self.state('zoomed')
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.geometry('{}x{}'.format(str(self.width), str(self.height)))
        self.title(title)
        self.update_idletasks()

        # GUI creation
        self.menu = Menu(self)
        self.status = Status(self)
        self.frame_start = FrameModeStart(self, width=self.width, height=self.height, bg=Styles.colors['background'])
        self.frame_sort = FrameModeSort(self, width=self.width, height=self.height, bg=Styles.colors['background'])
        self.frame_twin = FrameModeTwin(self, width=self.width, height=self.height, bg=Styles.colors['background'])
        self.mode_dict = {0: ('Start', self.frame_start), 1: ('Sort', self.frame_sort), 2: ('Twin', self.frame_twin)}

        # GUI initialization
        self.currentframe = self.mode_dict[0][1]
        self.status.statustext.set(self.mode_dict[0][0] + '-Mode')
        self.currentframe.pack()
        self.update_idletasks()
        self.resize()

        # Binds
        self.bind('<Left>', lambda e: self.left_key())
        self.bind('<Right>', lambda e: self.right_key())
        self.bind('<Up>', lambda e: self.up_key())
        self.bind('<Escape>', lambda e: self.cb_escape())

    def left_key(self):
        if self.currentframe == self.mode_dict[1][1]:
            self.frame_sort.shift_current_image(-1)

    def right_key(self):
        if self.currentframe == self.mode_dict[1][1]:
            self.frame_sort.shift_current_image(1)

    def up_key(self):
        if self.currentframe == self.mode_dict[1][1]:
            self.frame_sort.button_quickfuns_rotate_image()

    def cb_escape(self):
        self.destroy()

    def switch_mode(self, num):
        self.mode.set(num)
        self.status.statustext.set(self.mode_dict[num][0] + '-Mode')
        self.currentframe.pack_forget()
        self.mode_dict[num][1].pack(side="bottom", fill="both", expand=True)
        self.update_idletasks()
        self.currentframe = self.mode_dict[num][1]
        self.currentframe.on_activation()

    def resize(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.currentframe.config(width=self.width, height=self.height)


class FrameModeStart(tk.Frame):
    def __init__(self, root, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.root = root

    def on_activation(self):
        pass


class FrameModeSort(tk.Frame):
    def __init__(self, root, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.root = root

        self.validfiles = root.valid_photo_types
        self.photos = []

        # GUI settings
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=500)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(3, minsize=60)

        # area: display
        self.gridcell_displayed_image = tk.Frame(self)
        self.gridcell_displayed_image.grid(row=0, column=0, rowspan=3, sticky='nsew')
        self.gridcell_displayed_image.configure(bg='white', bd=1, relief='solid')
        self.frame_displayed_image = tk.Label(self.gridcell_displayed_image, bg=Styles.colors['widget_bg'])
        self.displayed_image = Photo(root.media_path, "girl_with_camera.png")
        self.frame_displayed_image.pack(fill='both', expand=1)
        self.set_displayed_image(self.displayed_image)

        # area: quickfuns
        self.gridcell_quickfuns = tk.Frame(self)
        self.gridcell_quickfuns.grid(row=3, column=0)
        self.quickfuns = [[0, 'Previous', lambda e: self.button_quickfuns_next_last("last")],
                          [1, 'Next', lambda e: self.button_quickfuns_next_last("next")],
                          [2, 'Rotate', lambda e: self.button_quickfuns_rotate_image()]]
        self.quickfun_buttons = []
        for fun in self.quickfuns:
            self.quickfun_buttons.append(self.prepare_quickfun_element(fun[0], fun[1], fun[2]))

        # area: workpath
        pad_wf = 20
        self.gridcell_workpath = tk.Frame(self, bg=Styles.colors['widget_bg'])
        self.gridcell_workpath.grid(row=0, column=1, sticky='nwe', pady=pad_wf, padx=pad_wf)
        self.workfolder = Path("empty")
        self.workpath_label = tk.Label(self.gridcell_workpath, text=self.workfolder, bg=Styles.colors['widget_bg']
                                       , fg=Styles.colors['font'])
        self.workpath_label.grid(column=0, row=0, sticky='EW')
        self.workpath_button = tk.Button(self.gridcell_workpath, text='change', relief="raised",
                                         bg=Styles.colors['widget_fg'], fg=Styles.colors['font'])
        self.workpath_button.grid(column=1, row=0)
        self.gridcell_workpath.columnconfigure(0, weight=1)
        self.workpath_button.bind('<Button-1>', lambda e: self.button_set_workpath())
        self.workpath_label.configure(text=str(self.workfolder))

        # area: metadata
        pad_md = 20
        self.gridcell_metadata = tk.Frame(self, pady=pad_md, padx=pad_md, bg=Styles.colors['background'])
        self.gridcell_metadata.grid(row=1, column=1, sticky="nesw")
        self.frame_metadata = tk.Frame(self.gridcell_metadata, bg=Styles.colors['widget_bg'])

        self.metadata_dict = {'oldname': [0, 'old name'],
                              'newname': [1, 'new name'],
                              'date': [2, 'date'],
                              'reso': [3, 'resolution']}

        for md_key in list(self.metadata_dict.keys()):
            self.metadata_dict[md_key].append(self.prepare_metadata_element(self.metadata_dict[md_key]))

        self.frame_metadata.columnconfigure(1, weight=5)
        self.frame_metadata.pack(fill="both", expand=True, side="left")

        # area: tags
        self.gridcell_tags = tk.Frame(self, pady=pad_md, padx=pad_md, bg=Styles.colors['background'])
        self.gridcell_tags.grid(row=2, column=1, sticky='ew')
        ttk.Combobox(self.gridcell_tags).grid(column=0, row=0, columnspan=2, sticky='ew')

    def prepare_quickfun_element(self, col, txt, fun):
        button_width = 20
        button_color = Styles.colors['widget_fg']
        font_color = Styles.colors['font']
        font_size = 8
        button = tk.Button(self.gridcell_quickfuns, width=button_width, text=txt)
        button.configure(bg=button_color, fg=font_color, font=font_size)
        button.grid(row=0, column=col)
        button.bind('<Button-1>', fun)
        return button

    def prepare_metadata_element(self, md_info):
        row = md_info[0]
        txt = md_info[1]
        ident = tk.Label(self.frame_metadata, text=txt, bg=Styles.colors['widget_fg'], fg=Styles.colors['font'])
        ident.grid(row=row, column=0, sticky="we")
        cont = tk.Label(self.frame_metadata, text='empty', bg=Styles.colors['widget_bg'], fg=Styles.colors['font'])
        cont.grid(row=row, column=1, sticky="we")
        return [ident, cont]

    def on_activation(self):
        self.set_displayed_image(self.displayed_image)

    def button_set_workpath(self):
        path = Path(tk.filedialog.askdirectory())
        self.workfolder = path
        self.workpath_label.configure(text=str(path))
        self.photos = self.scan_folder(path)
        self.set_displayed_image(self.photos[0])

    def scan_folder(self, path):
        files = os.listdir(path)
        photolist = []
        for img in files:
            if os.path.splitext(img)[1] in self.validfiles:
                photolist.append(Photo(path, img))
        return photolist

    def set_displayed_image(self, img):
        self.displayed_image = img
        image = get_resized_image(img.image, self.gridcell_displayed_image)
        image = ImageTk.PhotoImage(image)
        self.frame_displayed_image.config(image=image)
        self.frame_displayed_image.image = image

        if img in self.photos:
            self.metadata_dict['oldname'][2][1].config(text=img.oldname)
            self.metadata_dict['newname'][2][1].config(text='?')
            self.metadata_dict['date'][2][1].config(text=img.date)
            self.metadata_dict['reso'][2][1].config(text=img.reso)

    def button_quickfuns_next_last(self, cmd):
        if cmd == "next":
            self.shift_current_image(1)
        elif cmd == "last":
            self.shift_current_image(-1)

    def shift_current_image(self, dn):
        if self.displayed_image in self.photos:
            old_n = self.photos.index(self.displayed_image)
            new_n = old_n + dn
            if new_n < 0:
                new_n = len(self.photos) - 1
            elif new_n > len(self.photos) - 1:
                new_n = 0
            self.set_displayed_image(self.photos[new_n])

    def button_quickfuns_rotate_image(self):
        if self.displayed_image in self.photos:
            self.displayed_image.rotate()
            self.set_displayed_image(self.displayed_image)


class FrameModeTwin(tk.Frame):
    def __init__(self, root, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.root = root

    def on_activation(self):
        pass


class Menu(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.menu = tk.Menu(self.root, tearoff=False)
        self.root.config(menu=self.menu)

        self.submenu_start = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Start', menu=self.submenu_start)

        self.submenu_modes = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Modes', menu=self.submenu_modes)

        self.submenu_modes.add_command(label='Sort Photos', command=lambda: self.root.switch_mode(1))
        self.submenu_modes.add_command(label='Find Twins', command=lambda: self.root.switch_mode(2))


class Status(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.statustext = tk.StringVar()
        self.statustext.set('idle')
        self.status = tk.Label(self.root, textvariable=self.statustext, bd=1, relief='sunken', anchor='w')
        self.status.pack(side='bottom', fill='x')


class Photo:
    def __init__(self, path, img):
        self.oldname = img
        self.path = Path.joinpath(path, img)
        self.date = datetime.datetime.fromtimestamp(self.path.stat().st_mtime)
        self.tags = []
        self.image = Image.open(self.path)
        self.x, self.y = self.image.size
        self.reso = '{}x{}'.format(self.x, self.y)
        self.rotation = 0

    def rotate(self):
        self.rotation += 1
        if self.rotation >= 4:
            self.rotation = 0
        self.image = self.image.rotate(90, expand=True)


# ===== Static Functions =====
def get_resized_image(image, widget):
    x_i, y_i = image.size
    x_w, y_w = widget.winfo_width(), widget.winfo_height()
    ratio_i = x_i/y_i
    ratio_w = x_w/y_w
    if ratio_i >= ratio_w:
        img = image.resize((x_w, int(x_w/ratio_i)+1), Image.ANTIALIAS)
    else:
        img = image.resize((int(y_w*ratio_i), y_w), Image.ANTIALIAS)
    return img


def debug(obj_in):
    print('DEBUG > ' + str(obj_in))


# ===== Program =====
if __name__ == '__main__':
    app = TomSort('TomSort')
    app.mainloop()
