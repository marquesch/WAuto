from ui.window import Window, add_general_button_pack
from tkinter import ttk
import tkinter as tk

moodle_values = ['EAD', 'NX', 'Digital']
table_columns_added = ('disc_name', 'disc_moodle', 'ua1', 'ua2', 'ua3', 'ua4')
table_columns_headings = {'disc_name': 'Nome da disciplina',
                          'disc_moodle': 'Moodle',
                          'ua1': 'UA',
                          'ua2': 'UA',
                          'ua3': 'UA',
                          'ua4': 'UA'}

import_pos_dict_list = []


class ImportPosWindow(Window):
    def __init__(self):
        window_geometry = '600x530'

        super().__init__(window_geometry)

        self.add_title_label('H1', 'IMPORTAÇÃO UA SAGAH - PÓS GRADUAÇÃO')
        self.pack_title_frame()

        self.add_input_label('Nome da Disciplina', row=0, column=0, columnspan=4)
        self.add_input_label('Moodle', row=1, column=5)

        self.disc_name_entry = self.add_entry(row=1, column=0, columnspan=4, width=20)
        self.disc_moodle_combo_box = self.add_combo_box(moodle_values, row=2, column=5, width=7)

        self.ua_entry_list = []

        for i in range(4):
            self.add_input_label('UA', row=2, column=i)
            self.ua_entry_list.append(self.add_entry(row=3, column=i, width=5))

        self.add_general_button_grid(text='Adicionar', style='GeneralButton.TButton',
                                     command=self.add_disc_to_table, row=1, column=6, rowspan=3)

        self.input_frame.grid_columnconfigure('all', weight=1)
        self.input_frame.pack()

        self.disc_table = self.add_table(name='Fila de Importação',
                                         table_columns=table_columns_added,
                                         columns_display_dict=table_columns_headings,
                                         column_width=40)

        self.disc_table.bind('<Delete>', self.delete_items)

        self.disc_table.column('disc_name', width=240)

        self.table_frame.pack()

        self.check_box_value = self.add_check_box('Criar no Sagah')

        add_general_button_pack(self.main_frame, text='Iniciar\nImportação', style='ServiceButton.TButton',
                                padx=10, pady=15, command=self.run_service)

        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def delete_items(self, _):
        for item in self.disc_table.selection():
            item_index = self.disc_table.index(item)
            import_pos_dict_list.pop(item_index)
            self.disc_table.delete(item)

    def add_check_box(self, text):
        check_box_value = tk.BooleanVar(self.main_frame)
        new_check_box = ttk.Checkbutton(self.main_frame, text=text, onvalue=True, offvalue=False,
                                        variable=check_box_value)
        check_box_value.set(True)
        new_check_box.pack()
        return check_box_value

    def add_disc_to_table(self):
        ua_id_list = []
        disc_name = self.disc_name_entry.get()
        self.disc_name_entry.delete(0, tk.END)
        disc_moodle = self.disc_moodle_combo_box.get()
        self.disc_moodle_combo_box.delete(0, tk.END)
        for entry in self.ua_entry_list:
            ua_id = entry.get()
            if ua_id != '':
                ua_id_list.append(ua_id)
            entry.delete(0, tk.END)
        values = [disc_name, disc_moodle]
        for ua_id in ua_id_list:
            values.append(ua_id)
        self.disc_table.insert(parent='', index=tk.END, values=values)
        import_pos_grad_dict = {'disc_name': disc_name,
                                'disc_moodle': disc_moodle,
                                'disc_ua_list': ua_id_list}
        import_pos_dict_list.append(import_pos_grad_dict)

    def run_service(self):
        if self.check_box_value.get():
            from services.moodleservices import import_sagah_unities_pos_grad
            import_sagah_unities_pos_grad(import_pos_dict_list)
        else:
            from services.moodleservices import import_sagah_unities_pos_grad_created
            import_sagah_unities_pos_grad_created(import_pos_dict_list)
        self.destroy()
