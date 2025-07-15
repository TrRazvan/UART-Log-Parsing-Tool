import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import os

def launch_app(parse_func, live_func):
    def load_file():
        path = filedialog.askopenfilename()
        if not path:
            messagebox.showwarning("No File", "No file selected.")
            return

        try:
            df = parse_func(path)
            if df.empty:
                messagebox.showwarning("Empty File", "The parsed file is empty.")
                return
            display_df(df)
        except Exception as e:
            messagebox.showerror("Parsing Error", f"Failed to parse file:\n{str(e)}")

    def live_read():
        try:
            port = port_var.get()
            baudrate = int(baud_var.get())
            duration = int(duration_var.get())
            if not port:
                messagebox.showwarning("Missing Port", "Please enter a COM port.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Baudrate and duration must be numbers.")
            return

        try:
            df = live_func(port=port, baudrate=baudrate, duration=duration)
            if df.empty:
                messagebox.showwarning("Empty Capture", "No data was captured from the port.")
                return
            display_df(df)
        except Exception as e:
            messagebox.showerror("Live Read Error", f"Failed to read live UART:\n{str(e)}")

    def display_df(df):
        nonlocal current_df
        current_df = df.copy()

        try:
            os.makedirs("export", exist_ok=True)
            df.to_csv("export/parsed_log.csv", index=False)
        except Exception as e:
            messagebox.showwarning("Export Failed", f"Could not save CSV:\n{str(e)}")

        if not tree["columns"]:
            setup_columns(list(df.columns))

        update_table()

    def sort_column(col):
        nonlocal current_df, sort_reverse
        if col not in current_df.columns:
            messagebox.showwarning("Invalid Column", f"Column '{col}' not found in data.")
            return
        sort_reverse = not sort_reverse
        current_df = current_df.sort_values(by=col, ascending=not sort_reverse)
        update_table()

    def update_table():
        for row in tree.get_children():
            tree.delete(row)

        for _, row in current_df.iterrows():
            msg = str(row.get("Message", "")).upper()

            # Apply filter logic
            show = True
            if filter_mode.get() == "Error" and not is_error(msg):
                show = False
            elif filter_mode.get() == "Warning" and not is_warning(msg):
                show = False

            if not show:
                continue

            # Tag styling
            if is_error(msg):
                tag = 'error'
            elif is_warning(msg):
                tag = 'warning'
            else:
                tag = ''
            tree.insert("", "end", values=list(row), tags=(tag,))

    def is_error(msg):
        keywords = ["ERROR", "ERR", "FAIL", "EXCEPTION", "CRITICAL"]
        return any(kw in msg for kw in keywords)

    def is_warning(msg):
        keywords = ["WARN", "WARNING", "CAUTION", "ATTENTION"]
        return any(kw in msg for kw in keywords)

    def on_heading_click(col):
        return lambda: sort_column(col)

    def setup_columns(cols):
        tree["columns"] = cols
        tree["show"] = "headings"
        for col in cols:
            tree.heading(col, text=col, command=on_heading_click(col))
            tree.column(col, width=120)

        tree.tag_configure('error', background='tomato')
        tree.tag_configure('warning', background='khaki')

    def set_filter(mode):
        filter_mode.set(mode)
        update_table()

    # === GUI setup ===
    root = tk.Tk()
    root.title("UART Log Debug Tool")

    port_var = tk.StringVar(value="COM3")
    baud_var = tk.StringVar(value="9600")
    duration_var = tk.StringVar(value="10")
    filter_mode = tk.StringVar(value="All")

    frm_params = tk.Frame(root)
    frm_params.pack(padx=10, pady=5)

    tk.Label(frm_params, text="Port:").grid(row=0, column=0, sticky="e")
    tk.Entry(frm_params, textvariable=port_var, width=8).grid(row=0, column=1, padx=5)

    tk.Label(frm_params, text="Baudrate:").grid(row=0, column=2, sticky="e")
    tk.Entry(frm_params, textvariable=baud_var, width=8).grid(row=0, column=3, padx=5)

    tk.Label(frm_params, text="Duration (s):").grid(row=0, column=4, sticky="e")
    tk.Entry(frm_params, textvariable=duration_var, width=8).grid(row=0, column=5, padx=5)

    tk.Button(root, text="Parse Log File", command=load_file).pack(padx=20, pady=5)
    tk.Button(root, text="Live UART Capture", command=live_read).pack(padx=20, pady=5)

    # Filter buttons
    frm_filters = tk.Frame(root)
    frm_filters.pack(pady=5)

    tk.Label(frm_filters, text="Filter:").pack(side="left")

    tk.Button(frm_filters, text="All", command=lambda: set_filter("All")).pack(side="left", padx=5)
    tk.Button(frm_filters, text="Errors", command=lambda: set_filter("Error")).pack(side="left", padx=5)
    tk.Button(frm_filters, text="Warnings", command=lambda: set_filter("Warning")).pack(side="left", padx=5)

    # Table view
    tree = ttk.Treeview(root)
    tree.pack(fill="both", expand=True)

    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    current_df = pd.DataFrame()
    sort_reverse = False

    def on_heading_click(col):
        return lambda: sort_column(col)

    def setup_columns(cols):
        tree["columns"] = cols
        tree["show"] = "headings"
        for col in cols:
            tree.heading(col, text=col, command=on_heading_click(col))
            tree.column(col, width=120)

        tree.tag_configure('error', background='red')
        tree.tag_configure('warning', background='yellow')

    root.mainloop()
