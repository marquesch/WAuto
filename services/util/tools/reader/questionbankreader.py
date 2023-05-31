from services.util.tools.reader.filereader import read_file_as_list
import re

quest_regex = re.compile('\d+(\.|\))')
altern_regex = re.compile('([A-E]|[a-e])(\)|\.)')

just_start = ('Justificativa:',
              'Padrão de resposta:',
              'Resposta Padrão:',
              'Feedback')


def read_bank_txt(path: str) -> list:
    questions_list = []
    txt_list = read_file_as_list(path)
    i = 0

    while i < len(txt_list):
        unity_no = int(txt_list[i].strip('UNIDADE - \n'))
        i += 1

        while i < len(txt_list) \
                and quest_regex.match(txt_list[i]) is not None:
            question_no = int(txt_list[i][0:2].strip('.) \n'))
            question = {'no': question_no,
                        'name': '',
                        'statement': '',
                        'alternatives': [],
                        'feedback': '',
                        'correct': ''}
            if question_no < 10:
                question['name'] = ''.join(['Unidade 0',
                                            str(unity_no),
                                            ' - Questão 0',
                                            str(question_no)])
            else:
                question['name'] = ''.join(['Unidade 0',
                                            str(unity_no),
                                            ' - Questão ',
                                            str(question_no)])
            statement = txt_list[i][2:].lstrip('.) ').strip()
            i += 1
            while not altern_regex.match(txt_list[i]):
                statement += '\n' + txt_list[i].strip()
                i += 1
            question['statement'] = statement
            while altern_regex.match(txt_list[i]) is not None:
                alternative_name = txt_list[i][:1].strip().upper()
                alternative_body = txt_list[i][2:].strip()

                i += 1
                while not txt_list[i].startswith('CORRETA: ') \
                        and not txt_list[i].startswith(just_start) \
                        and altern_regex.match(txt_list[i]) is None:
                    alternative_body += '\n' + txt_list[i].strip()
                    i += 1
                alternative = {'name': alternative_name,
                               'body': alternative_body}
                question['alternatives'].append(alternative)
            if i < len(txt_list) and txt_list[i].startswith(just_start):
                feedback = txt_list[i].strip()
                i += 1
            else:
                feedback = ''
            while i < len(txt_list) \
                    and not txt_list[i].startswith('CORRETA: ') \
                    and not quest_regex.match(txt_list[i]):
                feedback += '\n' + txt_list[i].strip()
                i += 1
            question['feedback'] = feedback
            correct = txt_list[i][9]
            i += 1
            question['correct'] = correct

            questions_list.append(question)
    return questions_list


def print_bank(unities_list: list):
    for unity in unities_list:
        print('Unidade: ' + str(unity['no']))
        for question in unity['question_list']:
            print('Nome: ' + str(question['name']))
            print('Enunciado: ' + question['statement'])
            print('Alternativas: ')
            for alternative in question['alternatives']:
                if question['correct'] == alternative['name']:
                    print('CORRETA -', end='')
                print(alternative['name'] + ' ' + alternative['body'])
            print('Feedback: ' + question['feedback'])
            print('FIM QUESTAO\n')

