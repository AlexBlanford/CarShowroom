import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk


defaultCars = [
    {
        "make": "Toyota",
        "model": "Camry",
        "year": 2020,
        "price": 24000,
        "image": "camry.jpg"
    },
    {
        "make": "Honda",
        "model": "Civic",
        "year": 2019,
        "price": 22000,
        "image": "civic.jpg"
    },
    {
        "make": "Ford",
        "model": "Mustang",
        "year": 2021,
        "price": 30000,
        "image": "mustang.jpg"
    }
]

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
        if not cars:
            cars = defaultCars.copy()
            saveCars()
    except FileNotFoundError:
        cars = defaultCars.copy()
        saveCars()

def saveCars():
    with open(carFile, "w") as file:
        for car in cars:
            file.write(f"{car['make']},{car['model']},{car['year']},{car['price']},{car['image']}\n")
            
            
            
def showCars(sortOption=None):
    for widget in bottomFrame.winfo_children():
        widget.destroy()
        
    sortFrame = tk.Frame(bottomFrame)
    sortFrame.pack(fill="x", pady=(0, 20))

    sortDisplayayMap = {
        None: "Default Order",
        "price_asc": "Price: Low to High",
        "price_desc": "Price: High to Low",
        "alpha_asc": "A-Z (Alphabetical)",
        "alpha_desc": "Z-A (Reverse Alphabetical)",
        "year_asc": "Year: Oldest First",
        "year_desc": "Year: Newest First"
    }
        
    sortVar = tk.StringVar()
    
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
    
    cuurentDisplay = sortDisplayayMap.get(sortOption, "Default Order")
    sortVar.set(cuurentDisplay) 
    sortDropdown.pack(side="left", padx=5, pady=0)


    def applySort(event=None):
        
        optionMap = {v: k for k, v in sortDisplayayMap.items()}
            
        selectedOption = optionMap[sortVar.get()]
        showCars(selectedOption)


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


    canvas = tk.Canvas(bottomFrame)
    scrollBar = ttk.Scrollbar(bottomFrame, orient="vertical", command=canvas.yview)
    scrollableFrame = tk.Frame(canvas)
    
    canvas.configure(yscrollcommand=scrollBar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollBar.pack(side="right", fill="y")
    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")



    for i in range(len(displayCars)):
        car = displayCars[i]
        row = i // 3
        col = i % 3
        
        try:
            img = Image.open(car["image"])
            img = img.resize((220, 160), Image.Resampling.LANCZOS)
            imgTK = ImageTk.PhotoImage(img)
            
            carFrame = tk.Frame(scrollableFrame, bd=1, relief="groove", bg="white")
            carFrame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            imgLabel = tk.Label(carFrame, image=imgTK, bg="white")
            imgLabel.image = imgTK  
            imgLabel.pack()
            
            
            infoText = f"{car['make']} {car['model']}\nYear: {int(car['year'])}\nPrice: ${float(car['price']):,}"
            tk.Label(carFrame, text=infoText).pack()
        except Exception as e:
            print(f"Error loading image for {car['make']} {car['model']}: {e}")
            
            errorFrame = tk.Frame(scrollableFrame, bd=1, relief="groove", bg="white")
            errorFrame.grid(row=row, column=col, padx=10, pady=10)
            tk.Label(errorFrame, text=f"Error loading\n{car['make']} {car['model']}", bg="white").pack()
        
        
        for c in range(3):
            scrollableFrame.columnconfigure(c, weight=1)
        for r in range((len(displayCars) + 2) // 3):
            scrollableFrame.rowconfigure(r, weight=1)
        
    
    
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

