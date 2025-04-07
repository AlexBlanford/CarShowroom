import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw

BG_COLOR = "#faf9fa"
CAR_COLOR= "#ffffff"
PRIMARY_COLOR= "#2c3e50"
SECONDARY_COLOR= "#3498db"
ACCENT_COLOR= "#e74c3c"
TEXT_COLOR= "#2c3e50"
LIGHT_TEXT= "#ecf0f1"


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
        
    sortFrame = tk.Frame(bottomFrame, bg=BG_COLOR, pady=10)
    sortFrame.pack(fill="x")

    tk.Label(sortFrame, text="Sort By:", bg=BG_COLOR, fg=TEXT_COLOR, font=("Segoe UI", 10)).pack(side="left", padx=(20,5))
    
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground=CAR_COLOR, background=CAR_COLOR, foreground=TEXT_COLOR, bordercolor=PRIMARY_COLOR, arrowcolor=PRIMARY_COLOR, font=("Segoe UI", 9))
    
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
                               style='TCombobox',
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
            
            carFrame = tk.Frame(scrollableFrame, bg=CAR_COLOR, bd=0, highlightthickness=0, highlightbackground=PRIMARY_COLOR, width=240, height=220)
            carFrame.grid(row=row, column=col, padx=15, pady=15)
            carFrame.grid_propagate(False)
            
            shadow = tk.Frame(scrollableFrame, bg="#d5d8dc")
            shadow.grid(row=row, column=col, padx=15, pady=15, sticky = "nsew")
            shadow.lower(carFrame)
            
            carCanvas = tk.Canvas(carFrame, bg=CAR_COLOR, highlightthickness=0, width=250, height=250)
            carCanvas.pack()
            
            img = Image.open(car["image"])
            img = img.resize((230, 150), Image.Resampling.LANCZOS)
            
            mask = Image.new("L", (230,150), 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0, 0, 230, 150), radius=10, fill=255)
            img.putalpha(mask)
            
            imgTK = ImageTk.PhotoImage(img)
            carCanvas.create_image(125, 85, image=imgTK)
            
            carCanvas.create_text(125, 170, text=f"{car['make']} {car['model']}", font=("Segoe UI", 12, "bold"), fill=PRIMARY_COLOR)
            carCanvas.create_text(110, 190, text=f"Year: {car['year']} • ${float(car['price']):,}", font=("Segoe UI", 10), fill=SECONDARY_COLOR)
            
            
            def on_enter(e, frame = carFrame, shdw=shadow):
                carCanvas.configure(cursor="hand2")
                frame.configure(highlightthickness=2)
                shdw.configure(bg="b2babb", highlightbackground=PRIMARY_COLOR)
                
            def on_leave(e, frame = carFrame, shdw=shadow):
                carCanvas.configure(cursor="")
                frame.configure(highlightthickness=0)
                shdw.configure(bg="#d5d8dc")
            
            
            
            carCanvas.bind("<Enter>", on_enter)
            carCanvas.bind("<Leave>", on_leave)
            carCanvas.bind("<Button-1>", lambda e, c=car: showCarDetails(c))
            

            
            carCanvas.image = imgTK
            
        except Exception as e:
            print(f"Error loading image for {car['make']} {car['model']}: {e}")
            
            errorFrame = tk.Frame(scrollableFrame, bd=1, relief="groove", bg="white")
            errorFrame.grid(row=row, column=col, padx=10, pady=10)
            tk.Label(errorFrame, text=f"Error loading\n{car['make']} {car['model']}", bg="white", fg="red").pack()
            pass
        
        for c in range(3):
            scrollableFrame.columnconfigure(c, weight=1)
        for r in range((len(displayCars) + 2) // 3):
            scrollableFrame.rowconfigure(r, weight=1)
        
def showCarDetails(car):
    detailWindow = tk.Toplevel(root)
    detailWindow.title(f"{car['make']} {car['model']} Details")
    detailWindow.geometry("500x500")
    
    detailFrame = tk.Frame(detailWindow, padx=20, pady=20)
    detailFrame.pack(fill="both", expand=True)
    
    try:
        img = Image.open(car["image"])
        img = img.resize((350, 250), Image.Resampling.LANCZOS)
        imgTK = ImageTk.PhotoImage(img)
        imgLabel = tk.Label(detailFrame, image=imgTK)
        imgLabel.image = imgTK
        imgLabel.pack(pady=(0, 15))
    except Exception as e:
        tk.Label(detailFrame, text="Error loading image", font= ("Arial", 14), fg="red").pack(pady=(0, 15))
    
    
    infoText = f"Make: {car['make']}\nModel: {car['model']}\nYear: {int(car['year'])}\nPrice: ${float(car['price']):,}"
    tk.Label(detailFrame, text=infoText, font=("Arial", 14), justify="left").pack(pady=(0, 15))
    tk.Button(detailFrame, text="Close", command=detailWindow.destroy, bg="red", fg="white").pack(pady=(15, 0))


    
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

