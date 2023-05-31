import tkcalendar as tkc
import tkinter as tk
from tkinter import ttk


def add_general_button_pack(frame, text, style, command, padx=0, pady=0):
    new_button = ttk.Button(frame, text=text, style=style, command=command)
    new_button.pack(padx=padx, pady=pady)


def pack_frame_fill(frame: ttk.Frame):
    frame.pack(fill=tk.BOTH, expand=True)


def has_widget(frame, row, column):
    slaves = frame.grid_slaves(row=row, column=column)
    return len(slaves) > 0


class Window(tk.Tk):
    def __init__(self, geometry, window_title='WAuto'):
        super().__init__()
        self.main_frame = ttk.Frame(self)
        self.title_frame = ttk.Frame(self.main_frame)
        self.input_frame = ttk.Frame(self.main_frame)
        self.table_frame = ttk.Frame(self.main_frame)
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.geometry(geometry)
        self.resizable(False, False)
        self.title(window_title)
        style = ttk.Style(self)
        style.configure('H1.TLabel', font=('Roboto', 16, 'bold'), anchor='center', pady=0)
        style.configure('H2.TLabel', font=('Roboto', 14, 'bold'), anchor='center', pady=0)
        style.configure('H3.TLabel', font=('Roboto', 12, 'bold'), anchor='center', pady=0)
        style.configure('H4.TLabel', font=('Roboto', 10, 'bold'), anchor='center', pady=0)
        style.configure('H5.TLabel', font=('Roboto', 10), anchor='center', pady=0)
        style.configure('ServiceButton.TButton', font=('Roboto', 12), justify='center')
        style.configure('GeneralButton.TButton', font=('Roboto', 10), justify='center')

    def add_input_label(self, text, row, column, rowspan=1, columnspan=1, style='H4.TLabel', wraplength=0):
        new_label = ttk.Label(self.input_frame, style=style, text=text, wraplength=wraplength)
        new_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky='ew')
        return new_label

    def add_title_label(self, title_style, title_text, frame=None):
        if frame is None:
            frame = self.title_frame
        style = f'{title_style}.TLabel'
        title_label = ttk.Label(frame, style=style, text=title_text)
        title_label.pack(fill=tk.BOTH, expand=True)

    def add_general_button_grid(self, text, style, command, row, column, rowspan=1, columnspan=1):
        new_button = ttk.Button(self.input_frame, style=style, text=text, command=command)
        new_button.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=6, pady=4)

    def add_entry(self, row, column, width, columnspan=1):
        new_entry = ttk.Entry(self.input_frame, width=width, font=('Roboto', 9))
        new_entry.grid(row=row, column=column, columnspan=columnspan, padx=3, pady=3, sticky='ew')
        return new_entry

    def add_combo_box(self, values: list, row, column, columnspan=1, width=10):
        new_combo_box = ttk.Combobox(self.input_frame, values=values,
                                     width=width, height=1)
        new_combo_box.grid(row=row, column=column, columnspan=columnspan, padx=3, pady=3, sticky='ew')
        return new_combo_box

    def add_date_entry(self, row, column, columnspan=1, width=9):
        new_date_entry = tkc.DateEntry(self.input_frame, width=width, date_pattern='dd/mm/YY')
        new_date_entry.delete(0, tk.END)
        new_date_entry.grid(row=row, column=column, columnspan=columnspan, padx=3, pady=3)
        return new_date_entry

    def add_table(self, name, table_columns, columns_display_dict, column_width=80):
        new_label = ttk.Label(self.table_frame, style='H3.TLabel', text=name)
        new_label.pack(padx=10, pady=7)
        new_disc_table = ttk.Treeview(self.table_frame, columns=table_columns, show='headings')
        for column_display in columns_display_dict:
            new_disc_table.heading(column_display, text=columns_display_dict[column_display])
            new_disc_table.column(column_display, width=column_width)
            new_disc_table.column(column_display, anchor='center')
        new_disc_table.pack(fill=tk.BOTH, expand=True)
        return new_disc_table

    def pack_title_frame(self):
        self.title_frame.pack(padx=30, pady=20)
