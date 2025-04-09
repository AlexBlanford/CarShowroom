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
BTN_COLOR= "#3a5673"
BUTTON_HOVER= "#2980b9"
SHADOW_COLOR= "#d5d8dc"

TITLE_FONT = ("Segoe UI", 24, "bold")
HEADER_FONT = ("Segoe UI", 14, "bold")
BODY_FONT = ("Segoe UI", 11)
BTN_FONT = ("Segoe UI", 12, "bold")




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
root.attributes('-fullscreen', True)
root.configure(bg=BG_COLOR)

def toggleFull(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))
    
root.bind("<F11>", toggleFull)
root.bind("<Escape>", toggleFull)




cars = []


def loadCars():
    global cars
    try:
        with open(carFile, "r") as file:
            cars = []
            for line in file.readlines():
                parts = line.strip().split(",")
                if len(parts) >= 5:
                    cars.append({
                        "make": parts[0],
                        "model": parts[1],
                        "year": parts[2],
                        "price": parts[3],
                        "image": parts[4],
                        "mileage": parts[5] if len(parts) > 5 else "N/A",
                        "description": parts[6] if len(parts) > 6 else ""
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
            file.write(f"{car['make']},{car['model']},{car['year']},{car['price']},{car['image']},{car.get('mileage', 'N/A')},{car.get('description', '')}\n")
            
            
            
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
    
    screenWidth = root.winfo_width()
    columns = max(3, screenWidth // 300)



    for i in range(len(displayCars)):
        car = displayCars[i]
        row = i // columns
        col = i % columns
        
        try:
            img = Image.open(car["image"])
            img = img.resize((230, 150), Image.Resampling.LANCZOS)
            imgTK = ImageTk.PhotoImage(img)
            
            carFrame = tk.Frame(scrollableFrame, bg=CAR_COLOR, bd=0, highlightthickness=0, highlightbackground=PRIMARY_COLOR, width=240, height=220)
            carFrame.grid(row=row, column=col, padx=15, pady=15)
            carFrame.grid_propagate(False)
            
            shadow = tk.Frame(scrollableFrame, bg=SHADOW_COLOR)
            shadow.grid(row=row, column=col, padx=15, pady=15, sticky = "nsew")
            shadow.lower(carFrame)
            
            carCanvas = tk.Canvas(carFrame, bg=CAR_COLOR, highlightthickness=0, width=250, height=250)
            carCanvas.pack()
            
            
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
                shdw.configure(bg="#b2babb", highlightbackground=PRIMARY_COLOR)
                
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
        
        for c in range(columns):
            scrollableFrame.columnconfigure(c, weight=1)
            
        rows=(len(displayCars) + columns - 1) // columns
        for r in range(rows):
            scrollableFrame.rowconfigure(r, weight=1)
        
        def onResize(event):
            nonlocal columns
            newColumns = max(3, event.width // 300)
            if newColumns != columns:
                columns = newColumns
                showCars(sortOption)
                
        canvas.bind("<Configure>", onResize)
        
def showCarDetails(car):
    detailWindow = tk.Toplevel(root)
    detailWindow.title(f"{car['make']} {car['model']} ")
    detailWindow.geometry("620x730")
    
    header = tk.Canvas(detailWindow, height=80, bg=PRIMARY_COLOR, highlightthickness=0)
    header.pack(fill="x")
    
    for i in range(80):
        color = "#{:02x}{:02x}{:02x}".format(
            int(44*(1-i/80) + 52*i/80),
            int(62*(1-i/80) + 152*i/80),
            int(80*(1-i/80) + 219*i/80)
        )
        header.create_line(0, i, 600, i, fill=color)
        
    header.create_text(300, 40, text=f"{car['make']} {car['model']}", font=("Segoe UI", 20, "bold"), fill=LIGHT_TEXT) ####
    
    detailFrame = tk.Frame(detailWindow, padx=30, pady=30)
    detailFrame.pack(fill="both", expand=True)
    
    try:
        img = Image.open(car["image"])
        img = img.resize((400, 250), Image.Resampling.LANCZOS)
        imgTK = ImageTk.PhotoImage(img)
        
        imgLabel = tk.Label(detailFrame, image=imgTK, bg=BG_COLOR)
        imgLabel.image = imgTK
        imgLabel.pack(pady=(0, 20))
    except Exception as e:
        tk.Label(detailFrame, text="Error loading image", font= ("Segoe UI", 14), fg=ACCENT_COLOR, bg=BG_COLOR).pack()
    
    details = tk.Frame(detailFrame, bg=BG_COLOR)
    details.pack(fill="x")
    
    specs = [
        ("Year:", car["year"]),
        ("Price:", f"${float(car['price']):,}"),
        ("Mileage:", "30,000 km" if "mileage" not in car else f"{car['mileage']} km")
    ]
    
    for i, (label, value) in enumerate(specs):
        tk.Label(details,
                 text=label ,
                 font = ("Segoe UI", 12),
                 fg=TEXT_COLOR,
                 bg=BG_COLOR).grid(row=i, column=0, sticky="e", padx=(0, 10))
        
        tk.Label(details,
                 text=value,
                 font = ("Segoe UI", 12, "bold"),
                 fg=PRIMARY_COLOR,
                 bg=BG_COLOR).grid(row=i, column=1, sticky="w")
        
    tk.Label(details,
             text="Description:",
             font = ("Segoe UI", 12),
             fg=TEXT_COLOR,
             bg=BG_COLOR).grid(row=len(specs), column=0, sticky="ne", padx=(0, 10), pady=(10, 0))
    
    descText = car.get("description", "No description available.")
    description = tk.Text(details,
                        wrap="word",
                        font=("Segoe UI", 12),
                        bg=CAR_COLOR,
                        fg=TEXT_COLOR,
                        height=6,
                        width=40,
                        padx=10,
                        pady=10,
                        highlightthickness=0,
                        bd=0)
    description.insert("1.0", descText)
    description.config(state="disabled")
    description.grid(row=len(specs), column=1, sticky="w", pady=(10, 0))
        
    btnFrame = tk.Frame(detailFrame, bg=BG_COLOR, pady=20)
    btnFrame.pack()
    
    tk.Button(btnFrame,
              text="Close",
              bg=ACCENT_COLOR,
              fg="white",
              activebackground="#c0392b",
              font=("Segoe UI", 12, "bold"),
              padx=20,
              pady=3,
              bd=0,
              command=detailWindow.destroy).pack(side="left", padx=5)
              
              
                 
                 


    
def addCar():
    for widget in bottomFrame.winfo_children():
        widget.destroy()

    container = tk.Frame(bottomFrame, bg=BG_COLOR, padx=40, pady=30)
    container.pack(fill="both", expand=True)

    header = tk.Frame(container, bg=PRIMARY_COLOR)  
    header.pack(fill="x", pady=(0, 20))
    
    gradientCan = tk.Canvas(header, height=60, bg=PRIMARY_COLOR, highlightthickness=0)  
    gradientCan.pack(fill="x")
    
    width=800
    for i in range(60):
        r = int(44*(1-i/60) + 52*i/60)
        g = int(62*(1-i/60) + 152*i/60)
        b = int(80*(1-i/60) + 219*i/60)
        color = f"#{r:02x}{g:02x}{b:02x}"
        gradientCan.create_line(0, i, width, i, fill=color)
        
    gradientCan.create_text(width/2, 30, text="Add New Car", font=("Segoe UI", 18, "bold"), fill=LIGHT_TEXT)
    
    formShdw = tk.Frame(container, bg=SHADOW_COLOR)
    formShdw.pack(pady=(0, 20))
    
    formFrame = tk.Frame(formShdw, bg=CAR_COLOR, padx=30, pady=25)
    formFrame.pack(padx=3, pady=3)
    
    tk.Label(formFrame, text="* Required Fields", font=("Segoe UI", 9), fg=ACCENT_COLOR, bg=CAR_COLOR).grid(row=0, column=1, sticky="e", pady=(0,15))
    
    
    fields = [
        ("Make*:", "Toyota, Honda, etc."),
        ("Model*:", "Camdry, Civic, etc."),
        ("Year*:", "2020"),
        ("Price*:", "32000"),
        ("Mileage:", "30000"),
        ("Description:", "Vehicle details..."),
        ("Image Path*:", "car.jpg")
        ]
    entries = []
    
    for i, (label, placeholder) in enumerate(fields):
        lbl = tk.Label(formFrame, text=label, font=BODY_FONT, bg=CAR_COLOR, fg=TEXT_COLOR, anchor="w")
        lbl.grid(row=i+1, column=0, sticky="w", pady=5, padx=(0, 10))
        
        if label.endswith("*:"):
            lbl.config(fg=ACCENT_COLOR)
            
        if label == "Description:":
            entry = tk.Text(formFrame, height=5, width=40, font=BODY_FONT, bg=CAR_COLOR, fg=TEXT_COLOR, padx=10, pady=8, wrap="word", highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor=SECONDARY_COLOR)
            entry.insert("1.0", placeholder)
                
            
            def focusIn(event, widget=entry, ph=placeholder):
                if widget.get("1.0", "end-1c") == ph:
                    widget.delete("1.0", "end")
                    widget.config(fg=TEXT_COLOR)
                    
            def focusOut(event, widget=entry, ph=placeholder):
                if not widget.get("1.0", "end-1c"):
                    widget.insert("1.0", ph)
                    widget.config(fg="#95a5a6")
                    
            entry.bind("<FocusIn>", focusIn)
            entry.bind("<FocusOut>", focusOut)
            
            entry.grid(row=i+1, column=1, sticky = "ew", pady=5)
        else:
            entry = tk.Entry(formFrame, font=BODY_FONT, bg=CAR_COLOR, fg=TEXT_COLOR, highlightthickness=1, highlightbackground="#dfe6e9", highlightcolor=SECONDARY_COLOR)
            entry.insert(0, placeholder)
            
            def focusIn(event, widget=entry, ph=placeholder):
                if widget.get() == ph:
                    widget.delete(0, "end")
                    widget.config(fg=TEXT_COLOR)
                    
            def focusOut(event, widget=entry, ph=placeholder):
                if not widget.get():
                    widget.insert(0, ph)
                    widget.config(fg="#95a5a6")
                    
            entry.bind("<FocusIn>", focusIn)
            entry.bind("<FocusOut>", focusOut)
            
            entry.grid(row=i+1, column=1, sticky = "ew", pady=5, ipady=5)
            
        entries.append(entry)
        
    def browseImage():
        path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png"), ("All Files", "*.*")]
        )
        if path:
            entries[6].delete(0, "end")
            entries[6].insert(0, path)
            entries[6].config(fg=TEXT_COLOR)

        
    def createButton(parent, text, command, bgC = SECONDARY_COLOR, fgC = LIGHT_TEXT):
        btn = tk.Button(parent, text=text, command=command, bg=bgC, fg=fgC, activebackground=BUTTON_HOVER, activeforeground=LIGHT_TEXT, font=BTN_FONT, bd=0, padx=20, pady=10, relief=tk.FLAT, cursor="hand2")
        
        def onEnter(e):
            btn['background'] = BUTTON_HOVER
            
        def onLeave(e):
            btn['background'] = bgC
            
        btn.bind("<Enter>", onEnter)
        btn.bind("<Leave>", onLeave)
        return btn

    browseButton = createButton(formFrame, text="Browse Image", command=browseImage, bgC="#95a5a6", fgC=LIGHT_TEXT)
    browseButton.grid(row=6, column=2, padx=(10, 0), sticky="w")
    
    btnContainer = tk.Frame(container, bg=BG_COLOR)
    btnContainer.pack(pady=(10, 0))
    
    def submitCar():
        data = []
        
        for i, entry in enumerate(entries):
            if i ==5:
                content = entry.get("1.0", "end-1c")
                data.append(content if content != fields[i][1] else "")
            else:
                content = entry.get()
                data.append(content if content != fields[i][1] else "")
            
        reqFields = [0,1,2,3,4,5]
        missFields = []
        
        for i in reqFields:
            if not data[i] or data[i] == fields[i][1]:
                fieldName = fields[i][0].replace("*:", "")
                missFields.append(fieldName)
                entries[i].config(highlightbackground=ACCENT_COLOR, highlightcolor=ACCENT_COLOR)
            else:
                entries[i].config(highlightbackground="#dfe6e9", highlightcolor=SECONDARY_COLOR)
                
        if missFields:
            messagebox.showwarning(
                "Missing Information",
                f"Please fill in all required fields:\n{', '.join(missFields)}"
            )
            return
        
        try:
            Image.open(data[6])
        except Exception as e:
            messagebox.showerror("Invalid Image", "Please select a valid image file.")
            entries[6].config(highlightbackground=ACCENT_COLOR, highlightcolor=ACCENT_COLOR)
            return
        
        cars.append({
            "make": data[0],
            "model": data[1],
            "year": data[2],
            "price": data[3],
            "mileage": data[4] if data[4] and data[4] != fields[4][1] else "N/A",
            "description": data[5] if data[5] else "",
            "image": data[6]
        })
        
        saveCars()
        messagebox.showinfo("Success", "Car added successfully!")
        showCars()

    submitButton = createButton(btnContainer, text="Add Car", command=submitCar, bgC="#27ae60", fgC=LIGHT_TEXT)
    submitButton.pack(side="left", padx=10)
    
    cancelButton = createButton(btnContainer, text="Cancel", command=showCars, bgC=ACCENT_COLOR, fgC=LIGHT_TEXT)
    cancelButton.pack(side="left", padx=10)
    
    formFrame.columnconfigure(1, weight=1)
        
    

    



bottomFrame = tk.Frame(root)
bottomFrame.pack(side="bottom")
bottomFrame.pack(fill="both", expand=True, padx=20, pady=20)    

headerMain=tk.Frame(root, bg=PRIMARY_COLOR, height=80)
headerMain.pack(fill="x", pady=(0, 20))

titleLabel = tk.Label(headerMain, text="Premium Car Showroom", font=TITLE_FONT, bg=PRIMARY_COLOR, fg=LIGHT_TEXT)
titleLabel.pack(pady=20)


navFrame = tk.Frame(root, bg=BG_COLOR)
navFrame.pack(pady=(0, 20))

viewCarsButton = ttk.Button(navFrame, text="View Cars", command=showCars, style = 'TButton')
viewCarsButton.pack(side="left", padx=10)

addCarButton = ttk.Button(navFrame, text="Add Car", command=addCar, style = 'TButton')
addCarButton.pack(side="left", padx=10)








loadCars()
showCars()


root.mainloop()

