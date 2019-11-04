import tkinter as tk
import os
from pathlib import Path


class MainApplication(tk.Frame):
    def __init__(self, parent, title):
        tk.Frame.__init__(self, parent)
        self.root = parent
        self.mode = tk.IntVar()
        self.mode.set(0)    # start:0 sort:1 twin:2
        self.root.state('zoomed')
        self.root.title(title)

        self.menu = Menu(self)
        self.status = Status(self.root)

        self.frame_start = tk.Frame(self.root)
        self.frame_sort = tk.Frame(self.root)
        self.frame_twin = tk.Frame(self.root)
        self.currentframe = self.frame_start

    def updateinterface(self):
        print('updating interface - mode: ' + str(self.mode.get()))
        if self.mode.get() == 1:
            self.draw_mode_sort()
            print('Drawn: SortingMode')
        elif self.mode.get() == 2:
            self.draw_mode_twin()
            print('Drawn: TwinMode')

    def switch_frames(self, newframe):
        self.currentframe.pack_forget()
        self.currentframe = newframe
        newframe.pack(side="bottom", fill="both", expand=True)

    def draw_mode_sort(self):
        self.switch_frames(self.frame_sort)
        left_frame = tk.Frame(self.frame_sort, bg='blue', height=600, width=600)
        left_frame.pack(side='left', expand='0')
        right_frame = tk.Frame(self.frame_sort, bg='red', height=600, width=600)
        right_frame.pack(side='right', expand='0')

    def draw_mode_twin(self):
        self.switch_frames(self.frame_twin)
        self.frame_twin.pack(side="bottom", fill="both", expand=True)
        left_frame = tk.Frame(self.frame_twin, bg='green', height=600, width=600)
        left_frame.pack(side='left', expand='0')
        right_frame = tk.Frame(self.frame_twin, bg='yellow', height=600, width=600)
        right_frame.pack(side='right', expand='0')


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