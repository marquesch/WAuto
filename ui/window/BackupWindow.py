from ui.window import Window, add_general_button_pack
import tkinter as tk

disc_type_values = ['Produção', 'Sagah']
moodle_values = ['EAD', 'NX', 'Digital']
disc_area_values = ['EAH', 'GJS', 'GTC', 'PID', 'SBD']
table_columns_added = ('origin_moodle', 'origin_id', 'type', 'area', 'destination_moodle', 'destination_id')
table_columns_headings = {'origin_moodle': 'Mdl Origem',
                          'origin_id': 'ID Origem',
                          'type': 'Tipo',
                          'area': 'Área',
                          'destination_moodle': 'Mdl Destino',
                          'destination_id': 'ID Destino'}

backup_dict_list = []


class BackupWindow(Window):
    def __init__(self):
        window_geometry = '600x500'
        super().__init__(window_geometry)

        self.add_title_label('H1', 'IMPORTAR DISCIPLINA')
        self.pack_title_frame()

        self.add_input_label('Origem', row=0, column=0, columnspan=3)
        self.add_input_label('Destino', row=0, column=4, columnspan=2)

        self.add_input_label('Moodle', row=1, column=0)
        self.add_input_label('ID', row=1, column=1)
        self.add_input_label('Tipo', row=1, column=2)
        self.add_input_label('Área', row=1, column=3)
        self.add_input_label('Moodle', row=1, column=4)
        self.add_input_label('ID', row=1, column=5)

        self.origin_moodle_combo_box = self.add_combo_box(moodle_values, row=2, column=0, width=7)
        self.origin_disc_id_entry = self.add_entry(row=2, column=1, width=7)
        self.disc_type_combo_box = self.add_combo_box(disc_type_values, row=2, column=2)
        self.disc_area_combo_box = self.add_combo_box(disc_area_values, row=2, column=3)
        self.destination_moodle_combo_box = self.add_combo_box(moodle_values, row=2, column=4, width=7)
        self.destination_disc_id_entry = self.add_entry(row=2, column=5, width=5)

        self.add_general_button_grid(text='Adicionar', style='GeneralButton.TButton',
                                     command=self.add_disc_to_table, row=2, column=6)
        self.input_frame.grid_columnconfigure("all", weight=1)

        self.input_frame.pack()

        self.disc_table = self.add_table(name='Fila de Importação',
                                         table_columns=table_columns_added,
                                         columns_display_dict=table_columns_headings)

        self.disc_table.bind('<Delete>', self.delete_items)

        self.table_frame.pack()

        add_general_button_pack(self.main_frame, text='Iniciar\nImportação', style='ServiceButton.TButton',
                                padx=10, pady=15,
                                command=self.run_service)

        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def delete_items(self, _):
        for item in self.disc_table.selection():
            item_index = self.disc_table.index(item)
            backup_dict_list.pop(item_index)
            self.disc_table.delete(item)

    def add_disc_to_table(self):
        origin_moodle = self.origin_moodle_combo_box.get()
        self.origin_moodle_combo_box.delete(0, tk.END)
        origin_disc_id = self.origin_disc_id_entry.get()
        self.origin_disc_id_entry.delete(0, tk.END)
        disc_type = self.disc_type_combo_box.get()
        self.disc_type_combo_box.delete(0, tk.END)
        disc_area = self.disc_area_combo_box.get()
        self.disc_area_combo_box.delete(0, tk.END)
        destination_moodle = self.destination_moodle_combo_box.get()
        self.destination_moodle_combo_box.delete(0, tk.END)
        destination_disc_id = self.destination_disc_id_entry.get()
        self.destination_disc_id_entry.delete(0, tk.END)
        values = (origin_moodle, origin_disc_id, disc_type, disc_area, destination_moodle, destination_disc_id)
        self.disc_table.insert(parent='', index=tk.END, values=values)
        backup_dict = {'origin_moodle': origin_moodle,
                       'origin_id': origin_disc_id,
                       'disc_type': disc_type,
                       'disc_area': disc_area,
                       'destination_moodle': destination_moodle,
                       'destination_id': destination_disc_id}
        backup_dict_list.append(backup_dict)

    def run_service(self):
        from services import moodleservices
        moodleservices.multiple_back_up_and_restore(backup_dict_list)
        self.destroy()
