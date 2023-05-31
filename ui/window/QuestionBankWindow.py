from ui.window import Window, add_general_button_pack
from tkinter import filedialog
import tkinter as tk
import os

desktop_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
moodle_values = ['EAD', 'NX', 'Digital']
question_bank_dict = {'disc_moodle': '',
                      'disc_id': '',
                      'bank_file_path': ''}


class QuestionBankWindow(Window):
    def __init__(self):
        self.file_path = None
        window_geometry = '350x300'
        super().__init__(window_geometry)

        self.add_title_label('H1', 'BANCO DE QUESTÕES')
        self.pack_title_frame()

        self.add_input_label('Moodle', row=0, column=0)
        self.add_input_label('ID da Disciplina', row=0, column=1)

        self.disc_moodle_combo_box = self.add_combo_box(moodle_values, row=1, column=0)
        self.disc_id_entry = self.add_entry(row=1, column=1, width=7)
        self.file_path = ''
        self.add_general_button_grid(text='Anexar', style='GeneralButton.TButton',
                                     command=self.open_file, row=1, column=2)

        self.input_frame.grid_columnconfigure('all', weight=1)

        self.file_found_label = self.add_input_label('', row=2, column=0, columnspan=3)
        self.file_name_label = self.add_input_label('', row=3, column=0, columnspan=3, style='H5.TLabel',
                                                    wraplength=300)

        self.input_frame.pack()

        add_general_button_pack(self.main_frame, 'Iniciar', style='ServiceButton.TButton',
                                command=self.run_service,
                                padx=20, pady=20)

        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def open_file(self):
        self.file_path = filedialog.askopenfilename(initialdir=desktop_dir, title='Selecione o arquivo',
                                                    filetypes=(('arquivos .txt', '*.txt'), ('todos os aruivos', '*.*')))
        if self.file_path != '':
            self.file_found_label.configure(text='Arquivo encontrado!')
            self.file_name_label.configure(text=self.file_path)
            question_bank_dict['bank_file_path'] = self.file_path

    def run_service(self):
        question_bank_dict['disc_moodle'] = self.disc_moodle_combo_box.get()
        question_bank_dict['disc_id'] = self.disc_id_entry.get()
        if question_bank_dict['disc_id'] != '' and question_bank_dict['disc_moodle'] != '':
            from services.moodleservices import insert_questions_bank
            insert_questions_bank(question_bank_dict)

