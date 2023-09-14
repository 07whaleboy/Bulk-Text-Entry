import os
import time
import argparse
import random
import sys
import tkinter as tk
from tkinter import ttk

# Define the global variables
name_entry = None
contents_entry = None
instances_entry = None
nolog_var = None
confirmation_label = None
result_label = None
log_file_label = None
generate_button = None

def replace_random(text, random_nums):
    while '&random&' in text:
        random_num = str(random.randint(0, 32768))
        text = text.replace('&random&', random_num, 1)
        random_nums['&random&'] = random_num
    return text

def enable_generate_button(event=None):  # Updated
    try:
        instances = int(instances_entry.get())
        valid_instances = True
    except ValueError:
        valid_instances = False

    name = name_entry.get()
    contents = contents_entry.get()

    if name and contents and valid_instances:
        generate_button.config(state='normal')
    else:
        generate_button.config(state='disabled')

def generate_text():
    global name_entry, contents_entry, instances_entry, nolog_var, confirmation_label, result_label, log_file_label

    name = name_entry.get()
    contents = contents_entry.get()
    instances = int(instances_entry.get())
    nolog = nolog_var.get()

    num = 0
    lines_per_second = 0
    total_lines = 0

    if not os.path.exists('Output'):
        os.mkdir('Output')

    random_nums = {}  # Initialize random_nums dictionary

    name = replace_random(name, random_nums)  # Replace &random& in the file name

    if not nolog:
        log_file = f"Output/{name}_log.txt"
        log_file = replace_random(log_file, random_nums)  # Replace &random& in the log file name
        log = open(log_file, "w")
    else:
        log = None

    confirmation_message = f"This program will generate '{contents}' into '{name}' {instances} times when you press Generate."

    confirmation_label.config(text=confirmation_message)

    start_time = time.time()

    with open(f"Output/{name}.txt", "w") as file:
        if log:
            log.write("Start Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        for _ in range(instances):
            line = contents.replace('&linecount&', str(num + 1))
            line = replace_random(line, random_nums)  # Replace &random& in the content
            line += '\n'
            file.write(line)
            if log:
                log.write(f"Generated Line {num + 1}: {line}")
            num += 1
            total_lines += 1

    end_time = time.time()
    elapsed_time = end_time - start_time

    if elapsed_time > 0:
        lines_per_second = total_lines / elapsed_time
    else:
        lines_per_second = 0

    if log:
        log.write(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Elapsed Time: {elapsed_time:.2f} seconds\n")
        log.write(f"Average Lines Per Second: {lines_per_second:.2f} lines/s\n")
        log.close()

    result_label.config(text=f"Completed in {elapsed_time:.2f} seconds, with an average of {lines_per_second:.2f} lines per second.")
    if log:
        log_file_label.config(text=f"Log file '{log_file}' has been created.")

def main():
    try:
        global name_entry, contents_entry, instances_entry, nolog_var, confirmation_label, result_label, log_file_label, generate_button

        root = tk.Tk()
        root.title("Text Content Generator")

        # Create and configure the GUI elements
        frame = ttk.Frame(root, padding=10)
        frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="File Name:").grid(column=0, row=0, sticky=tk.W)
        name_entry = ttk.Entry(frame)
        name_entry.grid(column=1, row=0, sticky=(tk.W, tk.E))
        
        ttk.Label(frame, text="Text Content:").grid(column=0, row=1, sticky=tk.W)
        contents_entry = ttk.Entry(frame)
        contents_entry.grid(column=1, row=1, sticky=(tk.W, tk.E))
        
        ttk.Label(frame, text="Number of Instances:").grid(column=0, row=2, sticky=tk.W)
        instances_entry = ttk.Entry(frame)
        instances_entry.grid(column=1, row=2, sticky=(tk.W, tk.E))
        
        nolog_var = tk.BooleanVar()
        nolog_checkbutton = ttk.Checkbutton(frame, text="Disable Logging", variable=nolog_var)
        nolog_checkbutton.grid(column=1, row=3, sticky=tk.W)

        generate_button = ttk.Button(frame, text="Generate", command=generate_text, state='disabled')
        generate_button.grid(column=1, row=4, sticky=tk.E)

        confirmation_label = ttk.Label(frame, text="")
        confirmation_label.grid(column=0, row=5, columnspan=2, sticky=(tk.W, tk.E))

        result_label = ttk.Label(frame, text="")
        result_label.grid(column=0, row=6, columnspan=2, sticky=(tk.W, tk.E))

        log_file_label = ttk.Label(frame, text="")
        log_file_label.grid(column=0, row=7, columnspan=2, sticky=(tk.W, tk.E))

        # Bind entry change events to enable_generate_button function
        name_entry.bind("<KeyRelease>", lambda event: enable_generate_button())
        contents_entry.bind("<KeyRelease>", lambda event: enable_generate_button())
        instances_entry.bind("<KeyRelease>", lambda event: enable_generate_button())

        root.mainloop()

    except SystemExit as e:
        if e.code != 0:
            print("Switch invalid. Please use --help or -? for assistance.")
            sys.exit(1)

if __name__ == "__main__":
    main()
