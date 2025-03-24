import tkinter as tk
from tkinter import messagebox

root = tk.Tk()




titleName = tk.Label(root, text="Car Showroom", font=("Helvetica", 25))
titleName.pack(padx = 10, pady = 10)




tk.Button(root, text="View Cars", fg="blue", width=15, height = 2).pack(side="left", padx=10)
tk.Button(root, text="Add Car", fg="red", width = 15, height = 2).pack(side="left", padx=10)
frame = tk.Frame(root)
frame.pack(padx=10, pady=100, expand = True)


root.mainloop()