from services.util.tools.reader.infosreader import read_label_html
from services.util.tools.reader.filereader import read_file_as_string
from services.util.tools.reader.jsonreader import read_json
from services.util.tools.webdriverutil.moodledriverutil import MoodleDriverUtil
from services.util.tools.folderutil import wait_download
from services.util.tools.dateutil import get_date_dict
import os

apresentacao_alias = ['APRESENTAÇÃO', 'O QUE VOCÊ VAI ESTUDAR']
videoaulas_alias = ['VIDEOAULAS', 'ASSISTA ÀS AULAS']
forum_alias = ['FÓRUM', 'SE LIGA NESSE TEMA']
material_alias = ['MATERIAL', 'MATERIAIS']
tarefas_alias = ['TAREFAS', 'TAREFA']
praticas_alias = ['AULAS PRÁTICAS']
pesquisa_alias = ['PESQUISA', 'PESQUISA DA DISCIPLINA', 'AVALIAÇÃO DA DISCIPLINA']
saibamais_alias = ['SAIBA MAIS, SAIBAMAIS']
material_complementar_alias = ['MATERIAL COMPLEMENTAR']
audiobooks_alias = ['AUDIOBOOK', 'AUDIOBOOKS']
general_alias = ['GENERAL', 'GERAL', 'Geral']

aliases = [material_complementar_alias,
           apresentacao_alias,
           videoaulas_alias,
           audiobooks_alias,
           saibamais_alias,
           pesquisa_alias,
           material_alias,
           praticas_alias,
           general_alias,
           tarefas_alias,
           forum_alias]

main_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
imgs_path = os.path.join(main_path, 'img')
login_html_path = os.path.join(main_path, 'login.html')
moodle_cfg_path = os.path.join(main_path, 'cfg', 'moodle')
login_info_path = os.path.join(moodle_cfg_path, 'loginfo.json')
moodle_xpath_path = os.path.join(moodle_cfg_path, 'moodle_xpath.json')
sagah_xpath_path = os.path.join(moodle_cfg_path, 'sagah_xpath.json')
final_text_path = os.path.join(moodle_cfg_path, 'final.txt')
exam_text_path = os.path.join(moodle_cfg_path, 'exam.txt')
prod_nx_text_path = os.path.join(moodle_cfg_path, 'prod_nx.txt')
sagah_nx_text_path = os.path.join(moodle_cfg_path, 'sagah_nx.txt')
prod_ead_text_path = os.path.join(moodle_cfg_path, 'prod_ead.txt')
sagah_ead_text_path = os.path.join(moodle_cfg_path, 'sagah_ead.txt')
prod_dig_text_path = os.path.join(moodle_cfg_path, 'prod_dig.txt')
sagah_dig_text_path = os.path.join(moodle_cfg_path, 'sagah_dig.txt')
pos_grad_nx_text_path = os.path.join(moodle_cfg_path, 'posgrad_nx.txt')
pos_grad_ead_text_path = os.path.join(moodle_cfg_path, 'posgrad_ead.txt')
pos_grad_dig_text_path = os.path.join(moodle_cfg_path, 'posgrad_dig.txt')

xpaths = read_json(moodle_xpath_path)
login_info_dict = read_json(login_info_path)
moodle_username = login_info_dict['username']
moodle_password = login_info_dict['password']
test_password = login_info_dict['test_password']

course_general_html = {'Produção_EAD': read_file_as_string(prod_ead_text_path),
                       'Sagah_EAD': read_file_as_string(sagah_ead_text_path),
                       'Produção_Digital': read_file_as_string(prod_dig_text_path),
                       'Sagah_Digital': read_file_as_string(sagah_dig_text_path),
                       'Produção_NX': read_file_as_string(prod_nx_text_path),
                       'Sagah_NX': read_file_as_string(sagah_nx_text_path),
                       'Pós Graduação_EAD': read_file_as_string(pos_grad_ead_text_path),
                       'Pós Graduação_Digital': read_file_as_string(pos_grad_dig_text_path),
                       'Pós Graduação_NX': read_file_as_string(pos_grad_nx_text_path)}

downloads_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')

driver = MoodleDriverUtil(downloads_path)


def get_links_dict(moodle):
    home = ''
    rel_links = {'backup': 'backup/backup.php?id=',
                 'disc_link': 'course/view.php?id=',
                 'section_config': 'course/editsection.php?id=',
                 'tiles_image': 'course/format/tiles/editimage.php?courseid=',
                 'disc_config': 'course/edit.php?id=',
                 'quiz_config': 'course/modedit.php?update=',
                 'quiz_qlist': 'mod/quiz/edit.php?cmid=',
                 'course_index': 'course/index.php',
                 'add_external_lti': 'course/modedit.php?add=lti&type=&course=',
                 'add_label': 'course/modedit.php?add=label&type=&course=',
                 'new_question': 'question/question.php?qtype=multichoice&courseid=',
                 'question_bank': 'question/edit.php?courseid='}
    match moodle:
        case 'NX':
            home = 'https://lms.uniguairaca.agencianx.com.br/'
        case 'EAD':
            home = 'https://ead.uniguairaca.edu.br/'
        case 'Digital':
            home = 'https://digital.uniguairaca.edu.br/'
    for item in rel_links:
        rel_link = rel_links[item]
        rel_links[item] = home + rel_link
    rel_links['home'] = home
    return rel_links


def login_moodle(moodle):
    if moodle == 'NX':
        driver.open('file://' + login_html_path)
        driver.submit('name', 'submit')
        driver.wait_page_fully_load()
    else:
        links_dict = get_links_dict(moodle)
        driver.open(links_dict['home'])
        driver.wait_page_fully_load()
        if not driver.is_logged():
            driver.input_into('id', 'username', moodle_username)
            driver.input_into('id', 'password', moodle_password)
            driver.submit('id', 'password')


def find_disc_by_name(moodle, disc_name):
    links_dict = get_links_dict(moodle)
    course_index_link = links_dict['course_index']
    driver.open(course_index_link)
    driver.input_into('id', 'coursesearchbox', disc_name)
    driver.submit('id', 'coursesearchbox')
    driver.click('linktext', disc_name)
    disc_id = driver.get_element_value('name', 'id', 'value')
    return disc_id


def generate_backup(moodle, disc_id):
    links_dict = get_links_dict(moodle)
    backup_link = f"{links_dict['backup']}{str(disc_id)}"
    driver.open(backup_link)
    driver.click('id', 'id_setting_root_users')
    driver.click('id', 'id_oneclickbackup')
    driver.submit('name', 'contextid')
    backup_name = driver.get_text('css', '.cell.c0')
    driver.click('linktext', 'Download')
    return backup_name


def restore_backup(moodle, disc_id, backup_name):
    links_dict = get_links_dict(moodle)
    disc_link = f"{links_dict['disc_link']}{str(disc_id)}"
    driver.open(disc_link)
    restore_link = driver.get_element_value('xpath', xpaths[f'restore_file_{moodle}'], 'href')
    driver.open(restore_link)
    driver.click('name', 'backupfilechoose')
    wait_download(downloads_path, backup_name)
    location = os.path.join(downloads_path, backup_name)
    driver.upload_file('name', 'repo_upload_file', location)
    driver.click('css', '.fp-upload-btn')
    driver.wait_element_located('linktext', backup_name, 1200)
    driver.click('id', 'id_submitbutton')
    driver.submit('name', 'contextid')
    driver.restore_in_this_course()
    driver.submit('id', 'id_submitbutton')
    driver.select_by_text('id', 'id_setting_course_keep_roles_and_enrolments', 'Sim')
    driver.select_by_text('id', 'id_setting_course_keep_groups_and_groupings', 'Sim')
    driver.submit('id', 'id_submitbutton')
    driver.submit('id', 'id_submitbutton')
    driver.submit('name', 'id')


def set_tiles_format(moodle, disc_id):
    def get_format_name(disc_moodle):
        match disc_moodle:
            case 'EAD': return 'Formato Tiles'
            case 'NX': return 'Formato Blocos'
            case 'Digital': return 'Formato Tiles'

    links_dict = get_links_dict(moodle)
    disc_config_link = f"{links_dict['disc_config']}{str(disc_id)}"
    driver.open(disc_config_link)
    driver.wait_page_fully_load()
    driver.uncollapse_settings()
    tiles_format = get_format_name(moodle)
    driver.select_by_text('id', 'id_format', tiles_format)
    driver.wait_page_fully_load()
    driver.uncollapse_settings()
    if driver.get_element_value('id', 'id_courseusesubtiles', 'checked') is None:
        driver.click('id', 'id_courseusesubtiles')
    driver.submit('id', 'id_saveanddisplay')


def set_topics_format(moodle, disc_id):
    links_dict = get_links_dict(moodle)
    disc_config_link = f"{links_dict['disc_config']}{str(disc_id)}"
    driver.open(disc_config_link)
    driver.wait_page_fully_load()
    driver.uncollapse_settings()
    driver.select_by_text('id', 'id_format', 'Formato Tópicos')
    driver.wait_page_fully_load()
    driver.submit('id', 'id_saveanddisplay')


def add_sagah_unities_grad(moodle, disc_id, section,
                           unities_quantity, sagah_unities_dict):
    links_dict = get_links_dict(moodle)
    labels_html_list = read_label_html(moodle)
    count = 0
    for i in range(0, 4):
        index = count
        count += unities_quantity[i]
        add_label_link = f"{links_dict['add_label']}{str(disc_id)}&section={str(section)}"
        if unities_quantity[i] > 0:
            driver.open(add_label_link)
            driver.show_html_text_area('id_introeditor')
            driver.input_into('id', 'id_introeditor', labels_html_list[i])
            driver.click('id', 'id_submitbutton2')
        for j in range(index, count):
            unity_name, unity_link = list(sagah_unities_dict.items())[j]
            add_external_tool_link = f"{links_dict['add_external_lti']}{str(disc_id)}&section={str(section)}"
            driver.open(add_external_tool_link)
            driver.input_into('id', 'id_name', unity_name)
            driver.input_into('id', 'id_toolurl', unity_link)
            driver.click('id', 'id_submitbutton2')


def format_pos_grad_sagah(moodle, disc_id, unities_dict: dict):
    pos_grad_videos_html = course_general_html[f'Pós Graduação_{moodle}']
    links_dict = get_links_dict(moodle)
    set_topics_format(moodle, disc_id)
    general_label: str = driver.get_element_value('id', 'section-0', 'aria-labelledby')
    general_id = general_label.strip('sectionid-').rstrip('-title')
    general_config_link = f"{links_dict['section_config']}{str(general_id)}"
    driver.open(general_config_link)
    driver.show_html_text_area('id_summary_editor')
    driver.input_into('id', 'id_summary_editor', pos_grad_videos_html)
    driver.submit('id', 'id_submitbutton')
    activate_btn = driver.get_element_value('name', 'edit', 'value')
    if activate_btn == 'on':
        driver.submit('name', 'sesskey')
    no_of_topics = len(unities_dict)
    driver.click('class', 'add-sections')
    driver.modal_add_topics(no_of_topics)
    cont = 1
    for unity_name in unities_dict:
        section_element_id = f"section-{str(cont)}"
        add_external_tool_link = f"{links_dict['add_external_lti']}{str(disc_id)}&section={str(cont)}"
        driver.open(add_external_tool_link)
        driver.input_into('id', 'id_name', unity_name)
        driver.input_into('id', 'id_toolurl', unities_dict[unity_name])
        driver.click('id', 'id_submitbutton2')
        section_id = driver.get_element_value('id', section_element_id, 'aria-labelledby')
        section_id = section_id.lstrip('sectionid-').rstrip('-title')
        topic_config = f"{links_dict['section_config']}{str(section_id)}"
        driver.open(topic_config)
        driver.wait_page_fully_load(0.5)
        driver.click('id', 'id_name_customize')
        driver.input_into('id', 'id_name_value', unity_name)
        driver.click('id', 'id_submitbutton')
        cont += 1


def set_block_names_and_images(moodle, disc_id, course_type, disc_area=''):
    def block_type(old_name):
        for alias in aliases:
            if old_name in alias:
                return alias[0]
        return None

    links_dict = get_links_dict(moodle)
    disc_link = f"{links_dict['disc_link']}{str(disc_id)}"
    if not driver.is_current_url(disc_link):
        driver.open(disc_link)
    driver.wait_page_fully_load()
    tiles_dict = driver.get_tiles_dict()
    for tile_old_name in tiles_dict:
        tile_config_link = f"{links_dict['section_config']}{tiles_dict[tile_old_name]}"
        driver.open(tile_config_link)
        tile_name = block_type(tile_old_name)
        if tile_name is None:
            continue
        if tile_name == 'GENERAL':
            driver.show_html_text_area('id_summary_editor')
            driver.input_into('id', 'id_summary_editor', course_general_html[f'{course_type}_{moodle}'])
            driver.submit('id', 'id_submitbutton')
        else:
            driver.input_into('id', 'id_name_value', tile_name)
            driver.submit('id', 'id_submitbutton')
            edit_image_link = f"{links_dict['tiles_image']}{disc_id}&sectionid={tiles_dict[tile_old_name]}"
            driver.open(edit_image_link)
            img_file_name = f'{tile_name.lower()}.png'
            if tile_name in praticas_alias:
                img_file_name = f'{tile_name.lower} {disc_area.lower}.png'
            image_file_path = os.path.join(imgs_path, img_file_name)
            driver.click('name', 'tileimagefilechoose')
            driver.upload_file('name', 'repo_upload_file', image_file_path)
            driver.click('css', '.fp-upload-btn')
            driver.wait_element_located('linktext', img_file_name)
            driver.click('id', 'id_submitbutton')


def fix_quizzes(moodle, disc_id,
                final_open_date=None, final_close_date=None,
                exam_open_date=None, exam_close_date=None):
    def check_questions(quiz_name_inner):
        driver.wait_page_fully_load()
        print(f"{'-' * 4}{quiz_name_inner}")
        quiz_size = driver.number_of_questions()
        max_grade = float(driver.get_element_value('id', 'inputmaxgrade', 'value').replace(',', '.'))
        print(f"{'-' * 6}Valor: {max_grade}")
        if quiz_size == 0:
            print(f"{'-' * 8}Questionário vazio!")
        else:
            quiz_sum = float(driver.get_text('class', 'mod_quiz_summarks').replace(',', '.'))
            if quiz_sum != max_grade:
                driver.fix_questions_mark(max_grade)
            print(f"{'-' * 8}Ok")

    def format_test(test_type, open_date_dict=None, close_date_dict=None):
        description = ''
        match test_type:
            case 'exam':
                description = read_file_as_string(exam_text_path)
            case 'final':
                description = read_file_as_string(final_text_path)
        driver.uncollapse_settings()
        driver.wait_page_fully_load()
        driver.input_into('id', 'id_introeditoreditable', description)
        start_date_disabled = driver.get_element_value('id', 'id_timeopen_day', 'disabled')
        check_start = (start_date_disabled is None and open_date_dict is None) or (
                start_date_disabled is not None and open_date_dict is not None)
        if check_start:
            driver.click('id', 'id_timeopen_enabled')
        if open_date_dict is not None:
            driver.select_by_text('id', 'id_timeopen_day', str(open_date_dict['day']))
            driver.select_by_text('id', 'id_timeopen_month', open_date_dict['month'])
            driver.select_by_text('id', 'id_timeopen_year', str(open_date_dict['year']))
            driver.select_by_text('id', 'id_timeopen_hour', '00')
            driver.select_by_text('id', 'id_timeopen_minute', '00')
        end_date_disabled = driver.get_element_value('id', 'id_timeclose_day', 'disabled')
        check_end = (end_date_disabled is None and close_date_dict is None) or (
                end_date_disabled is not None and close_date_dict is not None)
        if check_end:
            driver.click('id', 'id_timeclose_enabled')
        if close_date_dict is not None:
            close_date_dict = get_date_dict(close_date_dict)
            driver.select_by_text('id', 'id_timeclose_day', str(close_date_dict['day']))
            driver.select_by_text('id', 'id_timeclose_month', close_date_dict['month'])
            driver.select_by_text('id', 'id_timeclose_year', str(close_date_dict['year']))
            driver.select_by_text('id', 'id_timeclose_hour', '23')
            driver.select_by_text('id', 'id_timeclose_minute', '59')
        time_limit_disabled = driver.get_element_value('id', 'id_timelimit_number', 'disabled')
        if time_limit_disabled is not None:
            driver.click('id', 'id_timelimit_enabled')
        driver.input_into('id', 'id_timelimit_number', '90')
        driver.select_by_text('id', 'id_timelimit_timeunit', 'minutos')
        driver.select_by_text('id', 'id_attempts', '1')
        driver.show_password()
        driver.input_into('id', 'id_quizpassword', test_password)
        driver.submit('id', 'id_submitbutton2')

    def match_quest_type(q_name: str):
        if q_name.startswith('Avaliação'):
            return 'final'
        if q_name.startswith('Exame'):
            return 'exam'
        if q_name.startswith('Quest'):
            return 'quiz'
        return None

    links_dict = get_links_dict(moodle)
    disc_link = f"{links_dict['disc_link']}{str(disc_id)}"
    if not driver.is_current_url(disc_link):
        driver.open(disc_link)
    driver.wait_page_fully_load()
    disc_title = driver.get_text('class', 'page-header-headings')
    quizzes_section = driver.get_quizzes_section()
    quizzes_section_link = f'{disc_link}&section={quizzes_section}'
    driver.open(quizzes_section_link)
    quiz_dict = driver.get_quiz_dict()
    print(disc_title)
    for item in quiz_dict:
        quiz_name = item
        quiz_id = quiz_dict[item]
        quiz_type = match_quest_type(quiz_name)
        quiz_qlist_link = f"{links_dict['quiz_qlist']}{str(quiz_id)}"
        driver.open(quiz_qlist_link)
        check_questions(quiz_name)
        if quiz_type == 'final':
            quiz_config_link = f"{links_dict['quiz_config']}{str(quiz_id)}"
            driver.open(quiz_config_link)
            final_open_date_dict = get_date_dict(final_open_date)
            final_close_date_dict = get_date_dict(final_close_date)
            format_test(quiz_type, final_open_date_dict, final_close_date_dict)
        if quiz_type == 'exam':
            quiz_config_link = f"{links_dict['quiz_config']}{str(quiz_id)}"
            driver.open(quiz_config_link)
            exam_open_date_dict = get_date_dict(exam_open_date)
            exam_close_date_dict = get_date_dict(exam_close_date)
            format_test(quiz_type, exam_open_date_dict, exam_close_date_dict)


def insert_bank(moodle, disc_id, question_list):
    def insert_question(question_dict):
        new_question_link = f"{links_dict['new_question']}{str(disc_id)}&category={str(category)}"
        driver.open(new_question_link)
        driver.input_into('id', 'id_name', question_dict['name'])
        driver.input_into('id', 'id_questiontexteditable', question_dict['statement'])
        driver.input_into('id', 'id_generalfeedbackeditable', question_dict['feedback'])
        no_of_alternatives = len(question_dict['alternatives'])
        for i in range(no_of_alternatives):
            alternative = question_dict['alternatives'][i]
            alternative_text_box_id = f'id_answer_{str(i)}editable'
            driver.input_into('id', alternative_text_box_id, alternative['body'])
            if alternative['name'] == question_dict['correct']:
                select_id = f'id_fraction_{str(i)}'
                driver.select_by_text('id', select_id, '100%')
        driver.submit('id', 'id_submitbutton')
    links_dict = get_links_dict(moodle)
    questions_link = f"{links_dict['question_bank']}{str(disc_id)}"
    driver.open(questions_link)
    category = driver.get_disc_question_category()
    for question in question_list:
        insert_question(question)


def driver_quit():
    driver.quit()
