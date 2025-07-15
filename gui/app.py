import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd

def launch_app(parse_func, live_func):
    def load_file():
        path = filedialog.askopenfilename()
        if not path:
            return
        df = parse_func(path)
        display_df(df)

    def live_read():
        try:
            port = port_var.get()
            baudrate = int(baud_var.get())
            duration = int(duration_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Baudrate and duration must be numbers")
            return
        
        df = live_func(port=port, baudrate=baudrate, duration=duration)
        display_df(df)

    def display_df(df):
        nonlocal current_df
        current_df = df.copy()
        df.to_csv("export/parsed_log.csv", index=False)
        update_table()

    def sort_column(col):
        nonlocal current_df, sort_reverse
        sort_reverse = not sort_reverse
        current_df = current_df.sort_values(by=col, ascending=not sort_reverse)
        update_table()

    def update_table():
        # Delete all the rows
        for row in tree.get_children():
            tree.delete(row)

        # Insert the new data
        for _, row in current_df.iterrows():
            msg = str(row.get("Message", "")).upper()
            if "ERROR" in msg or "ERR" in msg:
                tag = 'error'
            elif "WARN" in msg or "WARNING" in msg:
                tag = 'warning'
            else:
                tag = ''
            tree.insert("", "end", values=list(row), tags=(tag,))

    root = tk.Tk()
    root.title("UART Log Debug Tool")

    port_var = tk.StringVar(value="COM3")
    baud_var = tk.StringVar(value="9600")
    duration_var = tk.StringVar(value="10")

    frm_params = tk.Frame(root)
    frm_params.pack(padx=10, pady=5)

    tk.Label(frm_params, text="Port:").grid(row=0, column=0, sticky="e")
    tk.Entry(frm_params, textvariable=port_var, width=8).grid(row=0, column=1, padx=5)

    tk.Label(frm_params, text="Baudrate:").grid(row=0, column=2, sticky="e")
    tk.Entry(frm_params, textvariable=baud_var, width=8).grid(row=0, column=3, padx=5)

    tk.Label(frm_params, text="Duration (s):").grid(row=0, column=4, sticky="e")
    tk.Entry(frm_params, textvariable=duration_var, width=8).grid(row=0, column=5, padx=5)

    tk.Button(root, text="Parse Log File", command=load_file).pack(padx=20, pady=10)
    tk.Button(root, text="Live UART Capture", command=live_read).pack(padx=20, pady=10)

    # The table in principal windows
    tree = ttk.Treeview(root)
    tree.pack(fill="both", expand=True)

    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    current_df = pd.DataFrame()
    sort_reverse = False

    # Sort column on heading click
    def on_heading_click(col):
        return lambda: sort_column(col)

    # Set columns when data exists initially
    def setup_columns(cols):
        tree["columns"] = cols
        tree["show"] = "headings"
        for col in cols:
            tree.heading(col, text=col, command=on_heading_click(col))
            tree.column(col, width=120)

        tree.tag_configure('error', background='red')
        tree.tag_configure('warning', background='yellow')

    # First display of the table
    def display_df(df):
        nonlocal current_df
        current_df = df.copy()
        df.to_csv("export/parsed_log.csv", index=False)

        if not tree["columns"]:
            setup_columns(list(df.columns))

        update_table()

    root.mainloop()
