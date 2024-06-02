import csv
import time
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import tkinter.font as tkFont
import json


current_code = ""

def search():
    output.set(code.get())
    try:
        file = open(file_path_string.get(), mode = 'r', encoding = "utf-8-sig")    
    except:
        output.set("LOI FILE")
        return
    data = csv.reader(file)
    global current_code
    for row in data:
        if len(row) > 1:
            # print(f"\"{code.get()}\"")
            if row[1] == f"\"{code.get()}\"" or row[1] == code.get(): 
                current_code = row[1]
                name = "unknown" 
                if len(row) >= 3:
                    name = row[2]
                description = f"""
                ID: {row[0]}
                Code: {row[1]}
                Name: {name}
                """  
                output.set(description)
                # code.set("")
                output_status.config(background = "Green")
                status.set("Valid")
                
                with open('data.json', 'r') as f:
                    data = json.load(f)
                if data[current_code]["check"] == "Invalid":
                    status.set("Invalid")
                    output_status.config(background = "Red")
                return

    
    current_code = ""
    code.set("")
    status.set("Invalid")
    output_status.config(background = "Red")

def browse_file():
    file_path_string.set(filedialog.askopenfilename(filetypes=(("csv files","*.csv"),)))

window = tk.Tk()
window.title("Prom scanner - made by hieupham1103")

def search_bind(event = None):
    search()
    code.set("")
    code_input.focus()

def edit_size():
    output_label.config(font = ('Helvetica bold', int(output_size.get())))
    print(output_size.get())

def checkin(): 
    if current_code == "":
        return
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        data[current_code] = {"check": "Invalid"}
        
        with open('data.json', "w") as f:
            json.dump(data, f, indent=4)
        
    except:
        print("LOI")      
    
def uncheck():
    if current_code == "":
        return
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        data[current_code] = {"check": ""}
        
        with open('data.json', "w") as f:
            json.dump(data, f, indent=4)
        
    except:
        print("LOI") 
        

window.bind("<Return>", search_bind)


file_path_string = tk.StringVar()
file_path = tk.Label(master = window,
            text = ".....",
            font = ('Helvetica bold', 26),
            textvariable = file_path_string
            )
file_path.pack()
browse_button = tk.Button(window,
                          text="FILE",
                          font=('Helvetica bold', 20),
                          command = browse_file
                          )
browse_button.pack()


code = tk.StringVar()
input_frame = tk.Frame(master = window)
code_input = tk.Entry(master = input_frame,
                       font = ('Helvetica bold', 26),
                       textvariable = code
                       )
search_button = tk.Button(master = input_frame,
                           text = "Search",
                           font = ('Helvetica bold', 20),
                           command = search
                           )
input_frame.pack()
code_input.pack(side = 'left')
search_button.pack(side = 'left')

output_size_frame = tk.Frame(master = window)

output_size = ttk.Scale(master = output_size_frame,
                        from_ = 10,
                        to = 100,
                        )
output_size_button = tk.Button(master = output_size_frame,
                           text = "Refresh",
                           command = edit_size
                            )

output_size_frame.pack()
output_size.pack(side = 'left')
output_size_button.pack(side = 'left')


output_frame = tk.Frame(master = window)

output = tk.StringVar()
output_label = tk.Label(master = output_frame,
                         text = ".....",
                         font = ('Helvetica bold', 50),
                         textvariable = output,
                         justify = 'left'
                         )
status = tk.StringVar()
output_status = tk.Label(master = output_frame,
                         text = "status",
                         font = ('Helvetica bold', 100),
                         textvariable = status,
                         justify = 'right',
                         )
output_frame.pack()
output_label.grid(row = 0, column = 0, padx=100, pady=100)
output_status.grid(row = 0, column = 1, padx=100, pady=100)

check_frame = tk.Frame(master = window)
check_frame.pack(side = "top")

checkin_button = tk.Button(master = check_frame,
                           text = "Check In",
                           command = checkin,
                           font = ('Helvetica bold', 40),
                           ).pack(side = 'left')

uncheck_button = tk.Button(master = check_frame,
                           text = "Uncheck",
                           command = uncheck,
                           font = ('Helvetica bold', 40),
                           ).pack(side = 'left')

window.mainloop()