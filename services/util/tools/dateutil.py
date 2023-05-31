from datetime import datetime

months = [None,
          'janeiro',
          'fevereiro',
          'março',
          'abril',
          'maio',
          'junho',
          'julho',
          'agosto',
          'setembro',
          'outubro',
          'novembro',
          'dezembro']


def get_date_dict(date_string):
    try:
        date_obj = datetime.strptime(date_string, '%d/%m/%Y')
    except ValueError:
        return None
    except TypeError:
        return None
    day = date_obj.day
    month = months[date_obj.month]
    year = date_obj.year
    date_dict = {'day': day,
                 'month': month,
                 'year': year}
    return date_dict
