from ui import window
from ui.window import Window
import tkinter as tk
from tkinter import ttk

project_title = 'web-automations'

author = 'Carlos H. Marques'

author_github = 'github.com/marquesch'


def first_available_position(frame, rows, columns):
    for i in range(0, rows):
        for j in range(0, columns):
            if not window.has_widget(frame, i, j):
                return i, j
    return None


def run_question_bank_window():
    from ui.window.QuestionBankWindow import QuestionBankWindow
    question_bank_window = QuestionBankWindow()
    question_bank_window.mainloop()


def run_backup_window():
    from ui.window.BackupWindow import BackupWindow
    backup_window = BackupWindow()
    backup_window.mainloop()


def run_format_window():
    from ui.window.FormatWindow import FormatWindow
    format_window = FormatWindow()
    format_window.mainloop()


def run_import_pos_window():
    from ui.window.ImportPosWindow import ImportPosWindow
    import_pos_window = ImportPosWindow()
    import_pos_window.mainloop()


def run_import_grad_window():
    from ui.window.ImportGradWindow import ImportGradWindow
    import_grad_window = ImportGradWindow()
    import_grad_window.mainloop()


class MainWindow(Window):
    def __init__(self):
        super().__init__('300x320')

        self.add_title_label('H1', project_title)
        self.add_title_label('H3', author)
        self.add_title_label('H5', author_github)
        self.pack_title_frame()
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack()

        self.add_service_button('Cadastrar\nBanco', command=run_question_bank_window)
        self.add_service_button('Importar\nDisciplinas', command=run_backup_window)
        self.add_service_button('Formatar\nDisciplinas', command=run_format_window)
        self.add_service_button(' \n ')
        self.add_service_button('Importar\nSagah (Pós)', command=run_import_pos_window)
        self.add_service_button('Importar\nSagah (Grad)', command=run_import_grad_window)

        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def add_service_button(self, text, command=None):
        new_button = ttk.Button(self.buttons_frame, style='ServiceButton.TButton', text=text, command=command)
        row, column = first_available_position(self.buttons_frame, 4, 2)
        new_button.grid(row=row, column=column, padx=8, pady=6)
