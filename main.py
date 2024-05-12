import cv2 as cv
import csv
from pyzbar.pyzbar import decode
import time
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

SCAN_ON = False

cap = cv.VideoCapture(1)

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
                return

        
def scan_button():
    global SCAN_ON
    SCAN_ON = not SCAN_ON

def browse_file():
    file_path_string.set(filedialog.askopenfilename(filetypes=(("csv files","*.csv"),)))

window = tk.Tk()
window.title("Prom scanner")
# window.geometry('300x150')

file_path_string = tk.StringVar()
file_path = ttk.Label(master = window,
            text = ".....",
            textvariable = file_path_string
            )
file_path.pack()
browse_button = tk.Button(window, text="FILE", font=40, command = browse_file)
browse_button.pack()


camera_frame = ttk.LabelFrame(master = window)
camera_frame.pack()
camera = ttk.Label(master = camera_frame)
camera.pack()


code = tk.StringVar()
input_frame = ttk.Frame(master = window)
code_input = ttk.Entry(master = input_frame, textvariable = code)
search_button = ttk.Button(master = input_frame,
                           text = "Search",
                           command = search
                           )
scan = ttk.Button(master = input_frame,
                           text = "Scan",
                           command = scan_button
                           )
input_frame.pack()
code_input.pack(side = 'left')
search_button.pack(side = 'left')
scan.pack(side = 'left')


output = tk.StringVar()
output_label = ttk.Label(master = window,
                         text = ".....",
                         textvariable = output
                         )
output_label.pack()


def _scan():
    global SCAN_ON
    if not cap.isOpened() or not SCAN_ON:
        window.update()
        return
    
    img = cap.read()[1]
    img = cv.flip(img,1)
    data = decode(img)
    if len(data):
        SCAN_ON = False
        code.set(str(data[0].data.decode('utf-8')))
        search()
        window.update()
        return
    img = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(img,cv.COLOR_BGR2RGB)))
    camera['image'] = img
    window.update()

while True:
    _scan()
    