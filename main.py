import csv
from pyzbar.pyzbar import decode
import time
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
            

def search():
    output.set(code.get())
    try:
        file = open(file_path_string.get(), mode = 'r', encoding = "utf-8-sig")    
    except:
        output.set("LOI FILE")
    data = csv.reader(file)
    for row in data:
        if len(row) > 1:
            print(f"\"{code.get()}\"")
            if row[1] == f"\"{code.get()}\"" or row[1] == code.get(): 
                name = "unknown" 
                if len(row) >= 3:
                    name = row[2]
                description = f"""ID: {row[0]}
                Code: {row[1]}
                Name: {name}
                """  
                output.set(description)
                code.set("")
                return

    code.set("")

def browse_file():
    file_path_string.set(filedialog.askopenfilename(filetypes=(("csv files","*.csv"),)))

window = tk.Tk()
window.title("Prom scanner")
window.geometry('1000x800')

def search_enter(event):
    search()
window.bind('<Enter>',search_enter)



file_path_string = tk.StringVar()
file_path = ttk.Label(master = window,
            text = ".....",
            textvariable = file_path_string
            )
file_path.pack()
browse_button = tk.Button(window, text="FILE", font=40, command = browse_file)
browse_button.pack()


code = tk.StringVar()
input_frame = ttk.Frame(master = window)
code_input = ttk.Entry(master = input_frame, textvariable = code)
search_button = ttk.Button(master = input_frame,
                           text = "Search",
                           command = search
                           )
input_frame.pack()
code_input.pack(side = 'left')
search_button.pack(side = 'left')


output = tk.StringVar()
output_label = ttk.Label(master = window,
                         text = ".....",
                         font = 50,
                         textvariable = output
                         )
output_label.pack()

window.mainloop()