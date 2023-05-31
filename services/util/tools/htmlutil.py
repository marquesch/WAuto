from bs4 import BeautifulSoup
from collections import OrderedDict


def get_sagah_unities_dict(html_text):
    sagah_unities_dict = OrderedDict()
    soup = BeautifulSoup(html_text, 'lxml')
    ul_element = soup.find('ul')
    li_elements = ul_element.find_all('li')
    for unity in li_elements:
        pair = unity.find_all('p')
        name = pair[0].text
        link = pair[1].text
        sagah_unities_dict[name] = link
    return sagah_unities_dict
