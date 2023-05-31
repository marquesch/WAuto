import os

main_dirpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

ignore_line = ('\n', '#')


def read_label_html(moodle_name):
    moodle_cfg_path = os.path.join(main_dirpath, 'cfg', 'moodle')
    file_name = f'labels_{moodle_name}.txt'
    file_path = os.path.join(moodle_cfg_path, file_name)
    labels_list = []

    with open(file_path, 'r', encoding='utf-8') as file:
        html_tag = ''
        for line in file:
            if line.startswith(ignore_line):
                continue

            if line.endswith(('</p>\n', '</p>')):
                html_tag += line
                labels_list.append(html_tag)
                html_tag = ''
                continue

            else:
                html_tag += line

    return labels_list
