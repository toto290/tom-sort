import tkinter as tk
import os
from pathlib import Path


class MainApplication(tk.Frame):
    def __init__(self, parent, title):
        tk.Frame.__init__(self, parent)
        self.root = parent
        self.mode = tk.IntVar()
        self.mode.set(0)    # start:0 sort:1 twin:2
        #self.root.state('zoomed')
        self.root.geometry('1000x500')
        self.root.title(title)

        self.menu = Menu(self)
        self.status = Status(self.root)

        self.root.update()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()
        print('Frame root is ' + str(root_width) + ' wide and ' + str(root_height) + ' high')
        self.frame_start = FrameModeStart(self.root, width=root_width, height=root_height)
        self.frame_sort = FrameModeSort(self.root, width=root_width, height=root_height)
        self.frame_twin = FrameModeTwin(self.root, width=root_width, height=root_height)
        self.currentframe = self.frame_start
        self.updateinterface()

    def updateinterface(self):
        print('updating interface - mode: ' + str(self.mode.get()))
        self.currentframe.pack_forget()
        if self.mode.get() == 0:
            self.frame_start.packit()
            self.currentframe = self.frame_start
        elif self.mode.get() == 1:
            self.frame_sort.packit()
            self.currentframe = self.frame_sort
        elif self.mode.get() == 2:
            self.frame_twin.packit()
            self.currentframe = self.frame_twin


class FrameModeStart(tk.Frame):
    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.root = parent

    def packit(self):
        self.pack(side="bottom", fill="both", expand=True)


class FrameModeSort(tk.Frame):
    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.root = parent
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        print('Frame ModeSorting is ' + str(self.width) + ' wide and ' + str(self.height) + ' high')
        self.left_frame = tk.Frame(self, bg='blue', height=int(1 * self.height), width=int(0.7 * self.width))
        self.right_frame = tk.Frame(self, bg='red', height=int(1 * self.height), width=int(0.3 * self.width))
        self.left_frame.pack(side='left', expand='1')
        self.right_frame.pack(side='right', expand='1')

    def packit(self):
        print('Packed: SortingMode')
        self.pack(side="bottom", fill="both", expand=True)


class FrameModeTwin(tk.Frame):
    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.root = parent
        left_frame = tk.Frame(self, bg='green', height=600, width=600)
        right_frame = tk.Frame(self, bg='yellow', height=600, width=600)

    def packit(self):
        self.pack(side="bottom", fill="both", expand=True)



class Menu(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root)
        self.app = app
        self.menu = tk.Menu(app.root, tearoff=False)
        app.root.config(menu=self.menu)

        self.submenu_start = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Start', menu=self.submenu_start)

        self.submenu_modes = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Modes', menu=self.submenu_modes)
        self.submenu_modes.add_command(label='Sort Photos', command=self.activate_mode_sort)
        self.submenu_modes.add_command(label='Find Twins', command=self.activate_mode_twin)

    def activate_mode_sort(self):
        self.app.mode.set(1)
        self.app.status.statustext.set('Sorting Mode')
        print('Mode changed to: Sorting')
        self.app.updateinterface()
        
    def activate_mode_twin(self):
        self.app.mode.set(2)
        self.app.status.statustext.set('Twin Finding Mode')
        print('Mode changed to: TwinFinding')
        self.app.updateinterface()


class Status(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.statustext = tk.StringVar()
        self.statustext.set('idle')
        self.status = tk.Label(self.parent, textvariable=self.statustext, bd=1, relief='sunken', anchor='w')
        self.status.pack(side='bottom', fill='x')


'''
        self.screenX = self.root.winfo_screenmmwidth()
        self.screenY = self.root.winfo_screenheight()
'''

if __name__ == '__main__':
    root = tk.Tk()
    MainApplication(root, 'TomSort').pack(side="top", fill="both", expand=True)
    root.mainloop()

'''
workfolder = Path("C:/Users/tomod/Desktop/FotoSortTest")

filesInFolder = os.listdir(workfolder)
print(len(filesInFolder))
f = open(workfolder / Path(filesInFolder[2]))
print(f)
'''