from ui.window import Window, add_general_button_pack
import tkinter as tk

disc_type_values = ['Produção', 'Sagah']
moodle_values = ['EAD', 'NX', 'Digital']
disc_area_values = ['EAH', 'GJS', 'GTC', 'PID', 'SBD']
table_columns_added = ('disc_moodle', 'disc_id', 'type', 'area',
                       'final_open', 'final_close', 'exam_open', 'exam_close')
table_columns_headings = {'disc_moodle': 'Moodle',
                          'disc_id': 'ID',
                          'type': 'Tipo',
                          'area': 'Área',
                          'final_open': 'Av. Início',
                          'final_close': 'Av. Fim',
                          'exam_open': 'Ex. Início',
                          'exam_close': 'Ex. Fim'}

format_disc_dict_list = []


class FormatWindow(Window):
    def __init__(self):
        window_geometry = '700x550'

        super().__init__(window_geometry)
        self.add_title_label('H1', 'FORMATAÇÃO DE DISCIPLINAS')
        self.pack_title_frame()

        self.add_input_label('Disciplina', row=0, column=0, columnspan=3)

        self.add_input_label('Moodle', row=1, column=0)
        self.add_input_label('ID', row=1, column=1)
        self.add_input_label('Tipo', row=1, column=2)
        self.add_input_label('Área', row=1, column=3)

        self.disc_moodle_combo_box = self.add_combo_box(moodle_values, row=2, column=0, width=7)
        self.disc_id_entry = self.add_entry(row=2, column=1, width=7)
        self.disc_type_combo_box = self.add_combo_box(disc_type_values, row=2, column=2)
        self.disc_area_combo_box = self.add_combo_box(disc_area_values, row=2, column=3)

        self.add_input_label('Avaliação', row=3, column=0, columnspan=2)
        self.add_input_label('Exame', row=3, column=2, columnspan=2)

        self.add_input_label('Início', row=4, column=0)
        self.add_input_label('Fim', row=4, column=1)
        self.add_input_label('Início', row=4, column=2)
        self.add_input_label('Fim', row=4, column=3)

        self.final_open_date_entry = self.add_date_entry(row=5, column=0)
        self.final_close_date_entry = self.add_date_entry(row=5, column=1)
        self.exam_open_date_entry = self.add_date_entry(row=5, column=2)
        self.exam_close_date_entry = self.add_date_entry(row=5, column=3)

        self.add_general_button_grid(text='Adicionar', style='GeneralButton.TButton',
                                     command=self.add_disc_to_table, row=2, column=4, rowspan=4)

        self.input_frame.grid_columnconfigure('all', weight=1)
        self.input_frame.pack()

        self.disc_table = self.add_table(name='Fila de Formatação',
                                         table_columns=table_columns_added,
                                         columns_display_dict=table_columns_headings)

        self.disc_table.bind('<Delete>', self.delete_items)

        self.table_frame.pack()

        add_general_button_pack(self.main_frame, text='Iniciar\nFormatação', style='ServiceButton.TButton',
                                padx=10, pady=15, command=self.run_service)

        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def delete_items(self, _):
        for item in self.disc_table.selection():
            item_index = self.disc_table.index(item)
            format_disc_dict_list.pop(item_index)
            self.disc_table.delete(item)

    def add_disc_to_table(self):
        disc_moodle = self.disc_moodle_combo_box.get()
        self.disc_moodle_combo_box.delete(0, tk.END)
        disc_id = self.disc_id_entry.get()
        self.disc_id_entry.delete(0, tk.END)
        disc_type = self.disc_type_combo_box.get()
        self.disc_type_combo_box.delete(0, tk.END)
        disc_area = self.disc_area_combo_box.get()
        self.disc_area_combo_box.delete(0, tk.END)
        final_open = self.final_open_date_entry.get()
        self.final_open_date_entry.delete(0, tk.END)
        final_close = self.final_close_date_entry.get()
        self.final_close_date_entry.delete(0, tk.END)
        exam_open = self.exam_open_date_entry.get()
        self.exam_open_date_entry.delete(0, tk.END)
        exam_close = self.exam_close_date_entry.get()
        self.exam_close_date_entry.delete(0, tk.END)
        values = (disc_moodle, disc_id, disc_type, disc_area, final_open, final_close, exam_open, exam_close)
        self.disc_table.insert(parent='', index=tk.END, values=values)
        format_dict = {'disc_moodle': disc_moodle,
                       'disc_id': disc_id,
                       'disc_type': disc_type,
                       'disc_area': disc_area,
                       'final_open': final_open,
                       'final_close': final_close,
                       'exam_open': exam_open,
                       'exam_close': exam_close}
        format_disc_dict_list.append(format_dict)

    def run_service(self):
        from services.moodleservices import multiple_format_disc
        multiple_format_disc(format_disc_dict_list)
        self.destroy()
