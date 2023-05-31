from ui.window import Window, add_general_button_pack
import tkinter as tk

moodle_values = ['EAD', 'NX', 'Digital']
unity_values = ['1', '2', '3', '4']
table_columns_added = ('unity', 'ua1', 'ua2', 'ua3', 'ua4')
table_columns_headings = {'unity': 'Unidade',
                          'ua1': 'UA 1',
                          'ua2': 'UA 2',
                          'ua3': 'UA 3',
                          'ua4': 'UA 4'}
import_grad_dict = {'disc_name': '',
                    'disc_moodle': '',
                    'section': '',
                    'u1': [],
                    'u2': [],
                    'u3': [],
                    'u4': []}


class ImportGradWindow(Window):
    def __init__(self):
        geometry = '600x530'

        super().__init__(geometry)
        self.add_title_label('H1', 'IMPORTAÇÃO SAGAH (GRADUAÇÃO)')
        self.pack_title_frame()

        self.add_input_label('Nome da Disciplina', row=0, column=0, columnspan=4)
        self.add_input_label('Moodle', row=0, column=4)
        self.add_input_label('Section', row=0, column=5)

        self.disc_name_entry = self.add_entry(row=1, column=0, columnspan=4, width=20)
        self.disc_moodle_combo_box = self.add_combo_box(moodle_values, row=1, column=4, width=7)
        self.section_entry = self.add_entry(row=1, column=5, width=2)
        self.add_general_button_grid(text='Set', style='GeneralButton.TButton',
                                     command=self.set_disc_name_and_moodle, row=1, column=6)

        self.add_input_label('Unidade', row=2, column=0)
        self.disc_unity_combo_box = self.add_combo_box(unity_values, row=3, column=0, width=3)

        self.ua_entry_list = []

        for i in range(1, 5):
            self.add_input_label('UA', row=2, column=i)
            self.ua_entry_list.append(self.add_entry(row=3, column=i, width=5))

        self.add_general_button_grid(text='Adicionar', style='GeneralButton.TButton',
                                     command=self.add_unities_to_table, row=3, column=6)

        self.input_frame.columnconfigure('all', weight=1)
        self.input_frame.pack()

        self.disc_table = self.add_table(name='Unidades Sagah',
                                         table_columns=table_columns_added,
                                         columns_display_dict=table_columns_headings)

        self.disc_table.bind('<Delete>', self.delete_items)

        self.table_frame.pack()

        add_general_button_pack(self.main_frame, text='Iniciar\nImportação', style='ServiceButton.TButton',
                                padx=10, pady=15, command=self.run_service)

        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def delete_items(self, _):
        for item in self.disc_table.selection():
            unity_no = self.disc_table.item(item)['values'][0]
            import_grad_dict[f'u{str(unity_no)}'] = []
            self.disc_table.delete(item)

    def add_unities_to_table(self):
        ua_id_list = []
        unity_no = self.disc_unity_combo_box.get()
        self.disc_unity_combo_box.delete(0, tk.END)
        for entry in self.ua_entry_list:
            ua_id = entry.get()
            if ua_id != '':
                ua_id_list.append(ua_id)
            entry.delete(0, tk.END)
        values = [unity_no]
        for ua_id in ua_id_list:
            values.append(ua_id)
        self.disc_table.insert(parent='', index=tk.END, values=values)
        import_grad_dict[f'u{str(unity_no)}'] = ua_id_list

    def set_disc_name_and_moodle(self):
        import_grad_dict['disc_name'] = self.disc_name_entry.get()
        import_grad_dict['disc_moodle'] = self.disc_moodle_combo_box.get()
        import_grad_dict['section'] = self.section_entry.get()

    def run_service(self):
        unities = []
        unities.extend(import_grad_dict['u1'])
        unities.extend(import_grad_dict['u2'])
        unities.extend(import_grad_dict['u3'])
        unities.extend(import_grad_dict['u4'])
        import_grad_dict['unities'] = unities
        from services.moodleservices import import_sagah_unities_grad
        import_sagah_unities_grad(import_grad_dict)
        self.destroy()
