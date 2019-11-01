import tkinter as tk
import os
from pathlib import Path

appName = "TomSort"

root = tk.Tk()
root.title(appName)

# Frames
top_frame = tk.Frame(root).pack()
bottom_frame = tk.Frame(root).pack()

# Widgets
btn1 = tk.Button(top_frame, text="Sort Photos", bg="blue").pack()
btn2 = tk.Button(top_frame, text="Find Twins", bg="blue").pack()
btn3 = tk.Button(bottom_frame, text="404", fg="blue").pack(side="left")
btn4 = tk.Button(bottom_frame, text="404", fg="blue").pack(side="left")
root.

#root.mainloop()

workfolder = Path("C:/Users/tomod/Desktop/FotoSortTest")

filesInFolder = os.listdir(workfolder)
print(len(filesInFolder))
f = open(workfolder / Path(filesInFolder[2]))
print(f)