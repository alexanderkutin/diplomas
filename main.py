import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import sys
import threading

from certs import TextElement
from names import convert_names

NAME_X_OFFSET = 50
NAME_Y_OFFSET = 79
NUM_X_OFFSET = 40
NUM_Y_OFFSET = 134

# Redirect stdout to update in real-time within the Text widget
class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, output_text):
        self.text_widget.insert(tk.END, output_text)
        self.text_widget.see(tk.END)  # Auto-scroll to the end
        self.text_widget.update_idletasks()  # Refresh the widget

    def flush(self):
        pass  # No need to implement for this basic redirector


def worker(pdf_path, csv_path, out_folder, name_params, num_params):
    try:
        convert_names(pdf_path, csv_path, out_folder, name_params, num_params)
    finally:
        print("Done!")
        sys.stdout = sys.__stdout__  # Restore the original stdout after function execution


# Function to be executed when 'Run' is clicked
def run_function():
    pdf_path = pdf_path_var.get()
    csv_path = csv_path_var.get()
    output_folder = output_folder_var.get()

    name_params = TextElement(None, name_x_var.get(), name_y_var.get(), 35)
    num_params = TextElement(None, num_x_var.get(), num_y_var.get(), 20)

    if pdf_path and csv_path and output_folder:
        # Create a new window for output display
        output_window = Toplevel(root)
        output_window.title("Program Output")
        output_text = tk.Text(output_window, width=50, height=15)
        output_text.pack(padx=10, pady=10)

        # Redirect stdout to the Text widget
        sys.stdout = TextRedirector(output_text)

        # Run your_function in a separate thread
        threading.Thread(
            target=lambda: worker(csv_path, pdf_path, output_folder, name_params, num_params)).start()

    else:
        messagebox.showerror("Error", "Please select all required paths.")

# Function to select PDF file
def select_pdf():
    path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])
    pdf_path_var.set(path)

# Function to select CSV file
def select_csv():
    path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    csv_path_var.set(path)

# Function to select output folder
def select_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    output_folder_var.set(folder)

# Create the main window
root = tk.Tk()
root.title("File Path Selector")
root.geometry("600x420")

# Heading
heading_label = tk.Label(root, text="Select Files and Output Folder", font=("Arial", 14))
heading_label.grid(row=0, column=0, columnspan=3, pady=10)

# Variables to store paths
pdf_path_var = tk.StringVar()
csv_path_var = tk.StringVar()
output_folder_var = tk.StringVar()

# Offset variables with defaults matching TextElement construction
name_x_var = tk.IntVar(value=NAME_X_OFFSET)
name_y_var = tk.IntVar(value=NAME_Y_OFFSET)
num_x_var = tk.IntVar(value=NUM_X_OFFSET)
num_y_var = tk.IntVar(value=NUM_Y_OFFSET)

entry_style = {
    "width": 40,
    "bg": "#d3d3d3",
    "fg": "#111111",
    "insertbackground": "#111111",
}

# PDF file selection
tk.Label(root, text="PDF File:").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=pdf_path_var, **entry_style).grid(row=1, column=1)
tk.Button(root, text="Browse", command=select_pdf).grid(row=1, column=2, padx=5)

# CSV file selection
tk.Label(root, text="CSV File:").grid(row=2, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=csv_path_var, **entry_style).grid(row=2, column=1)
tk.Button(root, text="Browse", command=select_csv).grid(row=2, column=2, padx=5)

# Output folder selection
tk.Label(root, text="Output Folder:").grid(row=3, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=output_folder_var, **entry_style).grid(row=3, column=1)
tk.Button(root, text="Browse", command=select_output_folder).grid(row=3, column=2, padx=5)

# Name offset controls
tk.Label(root, text="Name X/Y Offset:").grid(row=4, column=0, padx=10, pady=5)
frame_name = tk.Frame(root)
frame_name.grid(row=4, column=1, sticky="w")
tk.Label(frame_name, text="X:").pack(side="left")
tk.Spinbox(frame_name, textvariable=name_x_var, from_=-500, to=500, width=6).pack(side="left", padx=(2, 10))
tk.Label(frame_name, text="Y:").pack(side="left")
tk.Spinbox(frame_name, textvariable=name_y_var, from_=-500, to=500, width=6).pack(side="left", padx=2)

# Number offset controls
tk.Label(root, text="Number X/Y Offset:").grid(row=5, column=0, padx=10, pady=5)
frame_num = tk.Frame(root)
frame_num.grid(row=5, column=1, sticky="w")
tk.Label(frame_num, text="X:").pack(side="left")
tk.Spinbox(frame_num, textvariable=num_x_var, from_=-500, to=500, width=6).pack(side="left", padx=(2, 10))
tk.Label(frame_num, text="Y:").pack(side="left")
tk.Spinbox(frame_num, textvariable=num_y_var, from_=-500, to=500, width=6).pack(side="left", padx=2)

# Run button
tk.Button(root, text="Run", command=run_function).grid(row=6, column=1, pady=20)

# Run the application
root.mainloop()
