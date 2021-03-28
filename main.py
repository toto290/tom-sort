import os
import datetime
import sqlite3
import tkinter as tk
import tkinter.filedialog
import debug_utilities_lib as dul

from debug_utilities_lib import debug
from settings import Settings, Styles
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Initial parameters
        self.mode = tk.StringVar()
        self.mode.set('Start')
        self.state('zoomed')
        self.update_idletasks()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.geometry('{}x{}'.format(str(self.width), str(self.height)))
        self.title('TomSort')
        self.update_idletasks()

        # GUI creation
        self.menu = Menu(self)
        self.status = Status(self)

        self.mode_dict = {'Start': StartView(self),
                          'Sort': SortView(self),
                          'Tag': TagView(self),
                          'Twin': TwinView(self)}

        # GUI initialization
        self.currentframe = self.mode_dict[self.mode.get()]
        self.status.statustext.set(str(self.mode.get()) + '-Mode')
        self.currentframe.pack()
        self.update_idletasks()
        self.resize()

        # Binds
        self.bind_keys()

    def switch_mode(self, mode_name):
        self.mode.set(mode_name)
        self.status.statustext.set(mode_name + '-Mode')
        self.currentframe.pack_forget()
        self.mode_dict[mode_name].pack(side="bottom", fill="both", expand=True)
        self.update_idletasks()
        self.currentframe = self.mode_dict[mode_name]
        self.currentframe.on_activation()
        self.bind_keys()

    def resize(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.currentframe.configure(width=self.width, height=self.height)

    def bind_keys(self):
        self.bind('<Left>', lambda e: self.currentframe.left_key())
        self.bind('<Right>', lambda e: self.currentframe.right_key())
        self.bind('<Up>', lambda e: self.currentframe.up_key())
        self.bind('<Escape>', lambda e: self.currentframe.cb_escape())


class View(tk.Frame):
    def __init__(self, root, **kwargs):
        tk.Frame.__init__(self, root, **kwargs)
        self.root = root
        self.config(width=root.width, height=root.height, bg=Styles.colors['background'])

    def left_key(self):
        dul.warning('left key pressed but no effect defined')

    def right_key(self):
        dul.warning('right key pressed but no effect defined')

    def up_key(self):
        dul.warning('up key pressed but no effect defined')

    def cb_escape(self):
        self.root.destroy()

    def on_activation(self):
        pass

    class ImageDisplayBox(tk.Frame):
        def __init__(self, root, **kwargs):
            tk.Frame.__init__(self, root, **kwargs)
            self.root = root
            self.configure(bg='white', bd=1, relief='solid')
            self.image_frame = tk.Label(self, bg=Styles.colors['widget_bg'])
            self.image = None
            self.image_frame.pack(fill='both', expand=1)

        def set_image(self, image):
            self.image = image
            image = get_resized_image(image, self)
            image = ImageTk.PhotoImage(image)
            self.image_frame.config(image=image)
            self.image_frame.image = image

    class ImageQuickfuns(tk.Frame):
        pass  # TODO

    class PathSelectionBox(tk.Frame):
        def __init__(self, root, callback_function, default_text='empty', **kwargs):
            tk.Frame.__init__(self, root, **kwargs)
            self.workfolder = None
            self.callback_function = callback_function
            self.root = root
            self.configure(bg=Styles.colors['widget_bg'])
            self.workpath_label = tk.Label(self, text=default_text, bg=Styles.colors['widget_bg'],
                                           fg=Styles.colors['font'])
            self.workpath_label.grid(column=0, row=0, sticky='EW')
            self.workpath_button = tk.Button(self, text='change', relief="raised", bg=Styles.colors['widget_fg'],
                                             fg=Styles.colors['font'])
            self.workpath_button.grid(column=1, row=0)
            self.workpath_button.bind('<Button-1>', lambda e: self.button_set_workpath())
            self.columnconfigure(0, weight=1)

        def button_set_workpath(self):
            path = Path(tk.filedialog.askdirectory())
            self.workfolder = path
            self.workpath_label.configure(text=str(path))
            self.callback_function(path)

    class MetaDataBox(tk.Frame):
        pass  # TODO


class StartView(View):
    def __init__(self, root, **kwargs):
        View.__init__(self, root, **kwargs)

        path_selection_box = View.PathSelectionBox(self, self.on_path_selection, 'no archive was selected')
        path_selection_box.grid(row=1, column=0, sticky='new', pady=int(root.height/3), padx=20)

        # GUI settings
        self.columnconfigure(0, weight=1, minsize=int(root.width/2))
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, minsize=60)

    def on_path_selection(self, path):
        debug('test')


class SortView(View):
    def __init__(self, root, **kwargs):
        View.__init__(self, root, **kwargs)

        self.photos = list()
        self.current_photo = Photo(Settings.media_path, 'default_placeholder.png')

        # GUI settings
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, minsize=500)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(3, minsize=60)

        # area: display
        self.image_display = View.ImageDisplayBox(self)
        self.image_display.grid(row=0, column=0, rowspan=3, sticky='nsew')

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
        self.workpath_box = View.PathSelectionBox(self, self.on_workpath_selection, 'empty')
        self.workpath_box.grid(row=0, column=1, sticky='nwe', pady=20, padx=20)

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
        self.set_displayed_photo(self.current_photo)

    def on_workpath_selection(self, path):
        self.photos = self.scan_folder(path)
        self.current_photo = self.photos[0]
        self.set_displayed_photo(self.current_photo)

    def scan_folder(self, path):
        files = os.listdir(path)
        photolist = []
        for img in files:
            if os.path.splitext(img)[1] in Settings.valid_image_types:
                photolist.append(Photo(path, img))
        return photolist

    def set_displayed_photo(self, photo):
        self.image_display.set_image(photo.image)
        self.current_photo = photo

        if photo in self.photos:
            self.metadata_dict['oldname'][2][1].config(text=photo.oldname)
            self.metadata_dict['newname'][2][1].config(text='?')
            self.metadata_dict['date'][2][1].config(text=photo.date)
            self.metadata_dict['reso'][2][1].config(text=photo.reso)

    def button_quickfuns_next_last(self, cmd):
        if cmd == "next":
            self.shift_current_image(1)
        elif cmd == "last":
            self.shift_current_image(-1)

    def shift_current_image(self, dn):
        if self.current_photo in self.photos:
            old_n = self.photos.index(self.current_photo)
            new_n = old_n + dn
            if new_n < 0:
                new_n = len(self.photos) - 1
            elif new_n > len(self.photos) - 1:
                new_n = 0
            self.set_displayed_photo(self.photos[new_n])

    def button_quickfuns_rotate_image(self):
        if self.current_photo in self.photos:
            self.current_photo.rotate()
            self.set_displayed_photo(self.current_photo)

    def left_key(self):
        self.shift_current_image(-1)

    def right_key(self):
        self.shift_current_image(1)

    def up_key(self):
        self.button_quickfuns_rotate_image()


class TagView(View):
    def __init__(self, root, **kwargs):
        View.__init__(self, root, **kwargs)


class TwinView(View):
    def __init__(self, root, **kwargs):
        View.__init__(self, root, **kwargs)


class Menu(View):
    def __init__(self, root):
        View.__init__(self, root)
        self.menu = tk.Menu(self.root, tearoff=False)
        self.root.config(menu=self.menu)

        self.submenu_start = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Start', menu=self.submenu_start)

        self.submenu_modes = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Modes', menu=self.submenu_modes)

        self.submenu_modes.add_command(label='Sort Photos', command=lambda: self.root.switch_mode('Sort'))
        self.submenu_modes.add_command(label='Tag Photos', command=lambda: self.root.switch_mode('Tag'))
        self.submenu_modes.add_command(label='Find Twins', command=lambda: self.root.switch_mode('Twin'))


class Status(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.statustext = tk.StringVar()
        self.statustext.set('idle')
        self.status = tk.Label(self.root, textvariable=self.statustext, bd=1, relief='sunken', anchor='w')
        self.status.pack(side='bottom', fill='x')


class Photo:
    def __init__(self, path, img_name):
        self.oldname = img_name
        self.path = Path.joinpath(path, img_name)
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
    if isinstance(image, Photo):
        image = image.image
    x_i, y_i = image.size
    x_w, y_w = widget.winfo_width(), widget.winfo_height()
    ratio_i = x_i/y_i
    ratio_w = x_w/y_w
    if ratio_i >= ratio_w:
        img = image.resize((x_w, int(x_w/ratio_i)+1), Image.ANTIALIAS)
    else:
        img = image.resize((int(y_w*ratio_i), y_w), Image.ANTIALIAS)
    return img


# ===== Program =====
if __name__ == '__main__':
    app = App()
    app.mainloop()
