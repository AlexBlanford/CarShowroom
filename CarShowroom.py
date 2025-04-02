import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk


carFile = "cars.txt"

root = tk.Tk()
root.title("Car Showroom")
root.geometry("900x700")




cars = []


def loadCars():
    global cars
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

def saveCars():
    with open(carFile, "w") as file:
        for car in cars:
            file.write(f"{car['make']},{car['model']},{car['year']},{car['price']},{car['image']}\n")
            
            
            
def showCars():
    for widget in bottomFrame.winfo_children():
        widget.destroy()

    for i in range(len(cars)):
        car = cars[i]
        row = i // 3
        col = i % 3
    
        img = Image.open(car["image"])
        img = img.resize((200, 150), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        
        carFrame = tk.Frame(bottomFrame, bd=2, relief="groove", padx=10, pady=10)
        carFrame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        imgLabel = tk.Label(carFrame, image=img)
        imgLabel.image = img  
        imgLabel.pack()
        
        
        info_text = f"{car['make']} {car['model']}\nYear: {car['year']}\nPrice: ${car['price']}"
        tk.Label(carFrame, text=info_text, font=("Arial", 12)).pack()
    

#add function next (for adding cars to show cars page)


titleName = tk.Label(root, text="Car Showroom", font=("Helvetica", 30, "bold"))
titleName.pack(pady=20)

bottomFrame = tk.Frame(root)
bottomFrame.pack(side="bottom")
bottomFrame.pack(fill="both", expand=True, padx=20, pady=20)    


tk.Button(root, text="View Cars", fg="blue", width=15, height = 3).pack(side="left", padx=10)
tk.Button(root, text="Add Car", fg="red", width = 15, height = 3).pack(side="left", padx=10)







loadCars()
showCars()


root.mainloop()

