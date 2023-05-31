def multiple_back_up_and_restore(backups_dict_list):
    from services.util import moodleutil
    for backup in backups_dict_list:
        origin_moodle = backup['origin_moodle']
        origin_id = backup['origin_id']
        disc_type = backup['disc_type']
        disc_area = backup['disc_area']
        destination_moodle = backup['destination_moodle']
        destination_id = backup['destination_id']
        moodleutil.login_moodle(origin_moodle)
        backup_file_name = moodleutil.generate_backup(origin_moodle, origin_id)
        if destination_moodle != origin_moodle:
            moodleutil.login_moodle(destination_moodle)
        moodleutil.restore_backup(destination_moodle, destination_id, backup_file_name)
        moodleutil.set_tiles_format(destination_moodle, destination_id)
        moodleutil.set_block_names_and_images(destination_moodle, destination_id, disc_type, disc_area)
    moodleutil.driver_quit()
    print("Backups concluídos com sucesso!")


def multiple_format_disc(format_disc_dict_list):
    from services.util import moodleutil
    for format_disc_dict in format_disc_dict_list:
        moodle = format_disc_dict['disc_moodle']
        disc_id = format_disc_dict['disc_id']
        disc_type = format_disc_dict['disc_type']
        disc_area = format_disc_dict['disc_area']
        final_open_date = format_disc_dict['final_open']
        final_close_date = format_disc_dict['final_close']
        exam_open_date = format_disc_dict['exam_open']
        exam_close_date = format_disc_dict['exam_close']
        moodleutil.login_moodle(moodle)
        moodleutil.set_tiles_format(moodle, disc_id)
        moodleutil.set_block_names_and_images(moodle, disc_id, disc_type, disc_area)
        moodleutil.fix_quizzes(moodle, disc_id, final_open_date, final_close_date, exam_open_date, exam_close_date)
    moodleutil.driver_quit()
    print("Formatações concluídas com sucesso!")


def insert_questions_bank(question_bank_dict):
    from services.util.tools.reader.questionbankreader import read_bank_txt
    from services.util import moodleutil
    txt_file_path = question_bank_dict['bank_file_path']
    moodle = question_bank_dict['disc_moodle']
    disc_id = question_bank_dict['disc_id']
    question_list = read_bank_txt(txt_file_path)
    moodleutil.login_moodle(moodle)
    moodleutil.insert_bank(moodle, disc_id, question_list)
    moodleutil.driver_quit()
    print("Banco de questões inserido com sucesso!")


def import_sagah_unities_pos_grad_created(import_pos_dict_list):
    from services.util import moodleutil
    from services.util.tools.htmlutil import get_sagah_unities_dict
    from services.util.emailutil import get_html_dict
    html_dict = get_html_dict(import_pos_dict_list, convert=True)
    for disc in import_pos_dict_list:
        moodle = disc['disc_moodle']
        disc_name = disc['disc_name']
        moodleutil.login_moodle(moodle)
        disc_unities_dict = get_sagah_unities_dict(html_dict[disc_name])
        disc_id = moodleutil.find_disc_by_name(moodle, disc_name)
        moodleutil.format_pos_grad_sagah(moodle, disc_id, disc_unities_dict)
    moodleutil.driver_quit()
    print("Importação concluída com sucesso")


def import_sagah_unities_pos_grad(import_pos_dict_list):
    from services.util import moodleutil
    from services.sagahservices import multiple_create_and_add_unities
    from services.util.tools.htmlutil import get_sagah_unities_dict
    from services.util.emailutil import get_html_dict
    sagah_created_disc = multiple_create_and_add_unities(import_pos_dict_list)
    html_dict = get_html_dict(disc_name_list=sagah_created_disc)
    for disc in import_pos_dict_list:
        moodle = disc['disc_moodle']
        disc_name = disc['disc_name']
        moodleutil.login_moodle(moodle)
        disc_unities_dict = get_sagah_unities_dict(html_dict[disc_name])
        disc_id = moodleutil.find_disc_by_name(moodle, disc_name)
        moodleutil.format_pos_grad_sagah(moodle, disc_id, disc_unities_dict)
    moodleutil.driver_quit()
    print("Importação concluída com sucesso")


def import_sagah_unities_grad(import_grad_dict):
    disc_name = import_grad_dict['disc_name']
    moodle = import_grad_dict['disc_moodle']
    section = import_grad_dict['section']
    unities_quantity = [len(import_grad_dict['u1']), len(import_grad_dict['u2']),
                        len(import_grad_dict['u3']), len(import_grad_dict['u4'])]
    sagah_unities = import_grad_dict['unities']
    from services.util import moodleutil
    from services.sagahservices import create_and_add_unities
    from services.util.tools.htmlutil import get_sagah_unities_dict
    from services.util.emailutil import get_html_dict
    create_and_add_unities(disc_name, sagah_unities, login=True, quit=True)
    html_unity_dict = get_html_dict([disc_name])
    sagah_unities_dict = get_sagah_unities_dict(html_unity_dict[disc_name])
    moodleutil.login_moodle(moodle)
    disc_id = moodleutil.find_disc_by_name(moodle, disc_name)
    moodleutil.add_sagah_unities_grad(moodle, disc_id, section,
                                      unities_quantity, sagah_unities_dict)
    moodleutil.driver_quit()
    print("Importação concluída com sucesso")

