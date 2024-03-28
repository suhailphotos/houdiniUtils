import tkinter as tk
from tkinter import filedialog

def open(button_index):
    file_path = filedialog.askopenfilename(initialdir='/', title='Select a file')
    if file_path:
        if button_index == 1:
            entry1.delete(0, tk.END)
            entry1.insert(0, file_path)
        elif button_index == 2:
            entry2.delete(0, tk.END)
            entry2.insert(0, file_path)

def import_action():
    #I plan on writing the code here 
    print("Importing...")
    if var_obj_context.get():
        print("Import into 'obj' context selected")
        # I plan on writing code here when 'obj' is selected
    if var_stage_context.get():
        print("Import into 'stage' context selected")
        # I plan on writing code here when 'stage' is selected

fspy = tk.Tk()
fspy.title('fSpy Camera Import')

# Labels
label1 = tk.Label(fspy, text="Select .json file:")
label2 = tk.Label(fspy, text="Select image file:")

button1 = tk.Button(fspy, text='Browse', bg='grey', command=lambda: open(1))
button2 = tk.Button(fspy, text='Browse', bg='grey', command=lambda: open(2))
entry1 = tk.Entry(fspy, bg='black', fg='white', width=40)
entry2 = tk.Entry(fspy, bg='black', fg='white', width=40)

var_obj_context = tk.BooleanVar()
var_stage_context = tk.BooleanVar()

checkbox_obj_context = tk.Checkbutton(fspy, text="Import into 'obj' context", variable=var_obj_context)
checkbox_stage_context = tk.Checkbutton(fspy, text="Import into 'stage' context", variable=var_stage_context)

import_button = tk.Button(fspy, text='Import', command=import_action)
cancel_button = tk.Button(fspy, text='Cancel', command=fspy.destroy)

# Layout
label1.grid(row=0, column=0, padx=10, pady=5, sticky='w')
button1.grid(row=0, column=1, padx=10, pady=5)
entry1.grid(row=0, column=2, padx=10, pady=5)

label2.grid(row=1, column=0, padx=10, pady=5, sticky='w')
button2.grid(row=1, column=1, padx=10, pady=5)
entry2.grid(row=1, column=2, padx=10, pady=5)

checkbox_obj_context.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky='w')
checkbox_stage_context.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky='w')

cancel_button.grid(row=4, column=1, padx=10, pady=10)
import_button.grid(row=4, column=2, padx=10, pady=10)

fspy.mainloop()

