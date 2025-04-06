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
    try:
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
    except FileNotFoundError:
        cars = []

def saveCars():
    with open(carFile, "w") as file:
        for car in cars:
            file.write(f"{car['make']},{car['model']},{car['year']},{car['price']},{car['image']}\n")
            
            
            
def showCars(sortOption=None):
    for widget in bottomFrame.winfo_children():
        widget.destroy()
        
    sortFrame = tk.Frame(bottomFrame)
    sortFrame.pack(fill="x", pady=(0, 20))

    carsFrame = tk.Frame(bottomFrame)
    carsFrame.pack(fill="both", expand=True)
        
    tk.Label(sortFrame, text="Sort by:").pack(side="left", padx=5)

    sortVar = tk.StringVar()
    sortVar.set("Default Order") 
    sortDropdown = ttk.Combobox(sortFrame, 
                               textvariable=sortVar,
                               values=[
                                   "Default Order",
                                   "Price: Low to High",
                                   "Price: High to Low",
                                   "A-Z (Alphabetical)",
                                   "Z-A (Reverse Alphabetical)",
                                   "Year: Oldest First",
                                   "Year: Newest First"
                               ],
                               state="readonly",
                               width=25)
    sortDropdown.pack(side="left", padx=5)
    sortDropdown.current(0)  

    def applySort(event=None):
            
        selectedOption = sortVar.get()  

        optionMap = {
            "Default Order": None,
            "Price: Low to High": "price_asc",
            "Price: High to Low": "price_desc",
            "A-Z (Alphabetical)": "alpha_asc",
            "Z-A (Reverse Alphabetical)": "alpha_desc",
            "Year: Oldest First": "year_asc",
            "Year: Newest First": "year_desc"
        }
        showCars(optionMap[sortVar.get()])
        sortKey = optionMap.get(selectedOption)
        print(f"Selected sorting: {selectedOption}, Sort key: {sortKey}")

    sortDropdown.bind("<<ComboboxSelected>>", applySort)
    
    displayCars = cars.copy()
    if sortOption == "price_asc":
        displayCars.sort(key=lambda x: float(x["price"]))
    elif sortOption == "price_desc":
        displayCars.sort(key=lambda x: float(x["price"]), reverse=True)
    elif sortOption == "alpha_asc":
        displayCars.sort(key=lambda x: f"{x['make']} {x['model']}")
    elif sortOption == "alpha_desc":
        displayCars.sort(key=lambda x: f"{x['make']} {x['model']}", reverse=True)
    elif sortOption == "year_asc":
        displayCars.sort(key=lambda x: int(x["year"]))
    elif sortOption == "year_desc":
        displayCars.sort(key=lambda x: int(x["year"]), reverse=True)




    for i in range(len(displayCars)):
        car = displayCars[i]
        row = i // 3
        col = i % 3
    
        img = Image.open(car["image"])
        img = img.resize((200, 150), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        
        carFrame = tk.Frame(carsFrame, bd=1, relief="groove")
        carFrame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        imgLabel = tk.Label(carFrame, image=img)
        imgLabel.image = img  
        imgLabel.pack()
        
        
        info_text = f"{car['make']} {car['model']}\nYear: {int(car['year'])}\nPrice: ${int(car['price']):,}"
        tk.Label(carFrame, text=info_text).pack()
        
        for c in range(3):
            carsFrame.columnconfigure(c, weight=1)
        for r in range((len(displayCars) + 2) // 3):
            carsFrame.rowconfigure(r, weight=1)
        
    
def addCar():
    for widget in bottomFrame.winfo_children():
        widget.destroy()

    tk.Label(bottomFrame, text="Add New Car", font=("Arial", 16, "bold")).pack(pady=10)

    fields = ["Make:", "Model:", "Year:", "Price:", "Image Path:"]
    entries = []
    for field in fields:
        frame = tk.Frame(bottomFrame)
        frame.pack(fill="x", padx=20, pady=5)
        tk.Label(frame, text=field, width=12, anchor="w").pack(side="left")
        entry = tk.Entry(frame, bg="lightgrey", fg="white")
        entry.pack(side="left", expand=True, fill="x")
        entries.append(entry)
        
    def browseImage():
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png")])
        if path:
            entries[4].delete(0, tk.END)
            entries[4].insert(0, path)

    browseButton = tk.Button(bottomFrame, text="Browse Image", command=browseImage)
    browseButton.pack(pady=5)
    
    def submitCar():
        data = [entry.get() for entry in entries]
        if not all(data):
            messagebox.showwarning("Error", "Please fill in all the fields!")
            return
        
        cars.append({
            "make": data[0],
            "model": data[1],
            "year": data[2],
            "price": data[3],
            "image": data[4]
        })
        saveCars()
        messagebox.showinfo("Success", "Car added successfully!")
        showCars()

    tk.Button(bottomFrame, text="Add Car", command=submitCar, bg="green", fg="black", font=("Arial", 12, "bold")).pack(pady=20)
    
    

    


titleName = tk.Label(root, text="Car Showroom", font=("Helvetica", 30, "bold"))
titleName.pack(pady=20)

bottomFrame = tk.Frame(root)
bottomFrame.pack(side="bottom")
bottomFrame.pack(fill="both", expand=True, padx=20, pady=20)    


tk.Button(root, text="View Cars", command = showCars, fg="blue", width=15, height = 3).pack(side="left", padx=10)
tk.Button(root, text="Add Car", command = addCar, fg="red", width = 15, height = 3).pack(side="left", padx=10)







loadCars()
showCars()


root.mainloop()

