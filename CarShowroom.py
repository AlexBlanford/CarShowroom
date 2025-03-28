import tkinter as tk
from tkinter import messagebox

carFile = "car_listings.txt"

root = tk.Tk()
root.title("Car Showroom")
root.geometry("900x700")



titleName = tk.Label(root, text="Car Showroom", font=("Helvetica", 30, "bold"))
titleName.pack(pady=20)

bottomFrame = tk.Frame(root)
bottomFrame.pack(side="bottom")
bottomFrame.pack(padx = 400, pady = 200)


tk.Button(root, text="View Cars", fg="blue", width=15, height = 3).pack(side="left", padx=10)
tk.Button(root, text="Add Car", fg="red", width = 15, height = 3).pack(side="left", padx=10)
frame = tk.Frame(root)
frame.pack(padx=10, pady=100, expand = True)


def loadCars():
    with open(carFile, "r") as file:
        cars = []
        for line in file.readlines():
            parts = line.strip().split(",")
            if len(parts) == 5:
                cars.append({
                    "make": parts[0],
                    "model": parts[1],
                    "year": parts[2],
                    "price": parts[3],
                    "image": parts[4]
                })

loadCars()
root.mainloop()

