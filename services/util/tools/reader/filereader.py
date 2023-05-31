ignore_line = ('#', '\n', '\xa0', '_')


def read_file_as_string(path):
    output = ''
    with open(path, 'r', encoding='utf8') as file:
        for line in file:
            if line.startswith(ignore_line):
                continue
            line = line.replace('\x09', ' ')
            output += line

    return output


def read_file_as_list(path):
    output = []
    with open(path, 'r', encoding='utf8') as file:
        for line in file:
            if line.startswith(ignore_line) or line.strip() == '':
                continue
            if line.startswith('\ufeff'):
                raise UnicodeError('UTF-8 with BOM encoding')
            line = line.replace('\x09', ' ').replace('()', '(  )')

            output.append(line)

    return output
