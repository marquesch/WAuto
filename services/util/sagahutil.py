from services.util.tools.webdriverutil.sagahdriverutil import SagahDriverUtil
from services.util.tools.reader.jsonreader import read_json
import os

links_dict = {'login': 'https://catalogo.grupoa.education/login',
              'home': 'https://catalogo.grupoa.education/home',
              'discipline': 'https://catalogo.grupoa.education/discipline',
              'current': 'https://catalogo.grupoa.education/current'}

main_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sagah_cfg_path = os.path.join(main_path, 'cfg', 'sagah')
sagah_xpath_path = os.path.join(sagah_cfg_path, 'sagah_xpath.json')
login_info_path = os.path.join(sagah_cfg_path, 'loginfo.json')

xpaths = read_json(sagah_xpath_path)

login_info_dict = read_json(login_info_path)
sagah_username = login_info_dict['username']
sagah_password = login_info_dict['password']

driver = SagahDriverUtil()


def login():
    driver.open(links_dict['login'])
    driver.wait_page_fully_load()
    driver.input_into('id', 'input-12', sagah_username)
    driver.input_into('id', 'input-13', sagah_password)
    driver.click('xpath', xpaths['login_btn'])
    driver.wait_page_fully_load()


def check_disc(disc_name):
    driver.open(links_dict['discipline'])
    driver.wait_page_fully_load()
    driver.input_into('xpath', xpaths['disc_filter'], disc_name)
    driver.element_enter('xpath', xpaths['disc_filter'])
    driver.wait_page_fully_load()
    return driver.check_disc_existence()


def create_disc(disc_name):
    driver.open(links_dict['discipline'])
    driver.wait_page_fully_load()
    driver.input_into('xpath', xpaths['new_disc'], disc_name)
    driver.input_into('xpath', xpaths['new_disc_course'], 'GERAL', clear=False)
    driver.click('xpath', xpaths['new_disc_btn'])


def edit_disc_size(disc_name, disc_size):
    driver.open(links_dict['current'])
    driver.wait_page_fully_load()
    driver.input_into('xpath', xpaths['curr_filter_disc'], disc_name)
    driver.element_enter('xpath', xpaths['curr_filter_disc'])
    driver.click('xpath', xpaths['edit_disc_size'])
    driver.input_into('xpath', xpaths['disc_size'], disc_size)
    driver.element_enter('xpath', xpaths['disc_size'])
    driver.open(links_dict['home'])
    driver.wait_page_fully_load()


def add_unity(disc_name, unity_code):
    driver.input_into('xpath', xpaths['search_unities'], unity_code)
    driver.element_enter('xpath', xpaths['search_unities'])
    driver.click('xpath', xpaths['add_unity_btn'])
    driver.input_into('xpath', xpaths['disc_filter_add'], disc_name)
    driver.element_enter('xpath', xpaths['disc_filter_add'])
    driver.click('xpath', xpaths['add_unity_to_disc'])
    driver.click('xpath', xpaths['close_add_unity'])
    driver.click('xpath', xpaths['close_toast_msg'])


def approve_disc(disc_name):
    driver.open(links_dict['current'])
    driver.wait_page_fully_load()
    driver.input_into('xpath', xpaths['curr_filter_disc'], disc_name)
    driver.element_enter('xpath', xpaths['curr_filter_disc'])
    driver.click('xpath', xpaths['expand_disc'])
    driver.click('xpath', xpaths['approve_disc'])
    driver.click('css', '.action-btn.mx-3.v-btn--contained')
    driver.click('xpath', xpaths['close_toast_msg'])
    driver.wait_page_fully_load()


def driver_quit():
    driver.quit()
