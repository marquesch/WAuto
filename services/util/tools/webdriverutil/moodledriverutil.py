import time

from services.util.tools.webdriverutil import DriverUtil, generate_xpath, get_by_type
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class MoodleDriverUtil(DriverUtil):
    def __init__(self, downloads_path):
        chrome_options = Options()
        prefs = {"download.default_directory": downloads_path,
                 'download.prompt_for_download': False,
                 'download.directory_upgrade': True,
                 'safebrowsing.enabled': True}
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("prefs", prefs)
        exe_path = "chromedriver.exe"
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "normal"
        super(MoodleDriverUtil, self).__init__(caps, chrome_options, exe_path)

    def is_logged(self):
        if len(self.driver.find_elements(By.ID, 'username')) > 0:
            return False
        return True

    def select_correct(self, select_id):
        select = Select(self.driver.find_element(By.ID, select_id))
        select.select_by_visible_text('100%')

    def number_of_questions(self):
        q_list = self.driver.find_elements(By.CSS_SELECTOR, '.activity.multichoice')
        return len(q_list)

    def fix_questions_mark(self, max_grade):
        q_list = self.driver.find_elements(By.CSS_SELECTOR, '.activity.multichoice')
        q_mark = max_grade/len(q_list)
        self.wait_page_fully_load()
        for question in q_list:
            q_xpath = generate_xpath(question)
            edit_mark = question.find_element(By.CLASS_NAME, 'editing_maxmark')
            edit_mark.click()
            mark_xpath = q_xpath + '/div/div/span[3]/span/form/input'
            self.wait_element_located('xpath', mark_xpath)
            mark_element = question.find_element(By.XPATH, mark_xpath)
            mark_element.send_keys(f"{str(q_mark)}")
            mark_element.submit()
            load_image_xpath = q_xpath + '/div/div/span[2]/img'
            self.wait_element_invisible('xpath', load_image_xpath)

    def get_tiles_dict(self):
        tiles_dict = {}
        self.wait_page_fully_load()
        tiles_list = self.driver.find_elements(By.CSS_SELECTOR, '.tile.tile-clickable')
        general_block_id = int(tiles_list[0].get_attribute('data-true-sectionid')) - 1
        tiles_dict['GENERAL'] = general_block_id
        for tile in tiles_list:
            tile_xpath = generate_xpath(tile)
            block_id = tile.get_attribute('data-true-sectionid')
            if self.get_element_value('xpath', tile_xpath, 'style') == '':
                block_name = tile.find_element(By.CLASS_NAME, 'tile-textinner').text
            else:
                block_name = tile.find_element(By.CLASS_NAME, 'photo-tile-text').text
            tiles_dict[block_name] = block_id
        return tiles_dict

    def get_quiz_dict(self):
        self.wait_page_fully_load()
        quiz_list = self.driver.find_elements(By.CSS_SELECTOR, '.activity.subtile.quiz.modtype_quiz')
        quiz_dict = {}
        for item in quiz_list:
            quiz_name = item.find_element(By.TAG_NAME, 'a').text.strip()
            quiz_id = int(item.get_attribute('data-cmid'))
            quiz_dict[quiz_name] = quiz_id
        return quiz_dict

    def get_quizzes_section(self):
        self.wait_page_fully_load()
        tiles_list = self.driver.find_elements(By.CSS_SELECTOR, '.tile.tile-clickable')
        for tile in tiles_list:
            if tile.text == 'TAREFAS':
                return tile.get_attribute('data-section')

    def modal_add_topics(self, no_of_topics):
        self.wait_page_fully_load(0.5)
        modal_element = self.driver.find_element(By.CLASS_NAME, 'modal-content')
        add_no_of_topics_field = modal_element.find_element(By.ID, 'add_section_numsections')
        add_no_of_topics_field.send_keys(str(no_of_topics))
        add_topics_element = modal_element.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        add_topics_element.click()
        self.wait_page_fully_load(0.5)

    def add_external_tool(self, section_element_id, external_tool_name):
        self.wait_page_fully_load(0.5)
        section_element = self.driver.find_element(By.ID, section_element_id)
        add_activity_element = section_element.find_element(By.CSS_SELECTOR, '.section-modchooser-link.btn.btn-link')
        add_activity_element.click()
        self.wait_page_fully_load(0.5)
        modal_box = self.driver.find_element(By.CLASS_NAME, 'modal-content')
        external_tool_element = modal_box.find_element(By.LINK_TEXT, external_tool_name)
        external_tool_element.click()
        self.wait_page_fully_load(0.5)

    def restore_in_this_course(self):
        restore_here_div = self.driver.find_element(By.CSS_SELECTOR, '.bcs-current-course.backup-section')
        click_radio = restore_here_div.find_element(By.ID, 'detail-pair-value-3')
        self.wait_element_clickable(By.ID, 'detail-pair-value-3')
        click_radio.click()
        continue_btn = restore_here_div.find_element(By.CSS_SELECTOR, '.btn.btn-primary')
        continue_btn.submit()

    def get_disc_question_category(self):
        div = self.driver.find_element(By.CLASS_NAME, 'createnewquestion')
        category_element = div.find_element(By.NAME, 'category')
        category = category_element.get_attribute('value')
        return category

    def show_password(self):
        script = '''
        var element = document.querySelector("#id_quizpassword");
            element.setAttribute('type', 'text');
        '''
        self.driver.execute_script(script)

    def uncollapse_settings(self):
        script = '''
        var elements = document.querySelectorAll("fieldset");
            elements.forEach(function(element) {
                element.setAttribute('class', 'clearfix collapsible');
            });
        '''
        self.driver.execute_script(script)

    def show_html_text_area(self, input_id):
        script = f'''
        var element = document.querySelector("#{input_id}");
        element.setAttribute('style', 'display: block');
        element.removeAttribute('hidden');
        '''
        self.driver.execute_script(script)
