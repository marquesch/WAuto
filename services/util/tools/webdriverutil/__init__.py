import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


def generate_xpath(child_element, current=''):
    child_tag = child_element.tag_name
    if child_tag == "html":
        return "/html[1]" + current
    parent_element = child_element.find_element(By.XPATH, "..")
    children_elements = parent_element.find_elements(By.XPATH, "*")
    count = 0
    for children_element in children_elements:
        children_element_tag = children_element.tag_name
        if child_tag == children_element_tag:
            count += 1
        if child_element == children_element:
            return generate_xpath(parent_element, "/" + child_tag + "[" + str(count) + "]" + current)
    return None


def get_by_type(bytype):
    by_type = By.ID
    match bytype:
        case "id":
            by_type = By.ID
        case "name":
            by_type = By.NAME
        case "tagname":
            by_type = By.TAG_NAME
        case "class":
            by_type = By.CLASS_NAME
        case "xpath":
            by_type = By.XPATH
        case "linktext":
            by_type = By.LINK_TEXT
        case "css":
            by_type = By.CSS_SELECTOR
    return by_type


class DriverUtil:
    def __init__(self, caps, chrome_options, exe_path):
        self.driver = webdriver.Chrome(desired_capabilities=caps,
                                       options=chrome_options,
                                       executable_path=exe_path)

    def implicitly_wait(self, time_wait):
        self.driver.implicitly_wait(time_wait)

    def wait_element_located(self, bytype, identification, wait_time=120):
        by_type = get_by_type(bytype)

        ready = WebDriverWait(self.driver, wait_time).until(
            EC.presence_of_element_located((by_type, identification)))
        return ready

    def wait_element_unlocated(self, bytype, identification, wait_time=120):
        by_type = get_by_type(bytype)

        ready = WebDriverWait(self.driver, wait_time).until_not(
            EC.presence_of_element_located((by_type, identification)))
        return ready

    def wait_element_clickable(self, bytype, identification, wait_time=120):
        by_type = get_by_type(bytype)

        ready = WebDriverWait(self.driver, wait_time).until(
            EC.element_to_be_clickable((by_type, identification)))
        return ready

    def wait_element_visible(self, bytype, identification, wait_time=120):
        by_type = get_by_type(bytype)

        ready = WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_all_elements_located((by_type, identification)))
        return ready

    def wait_element_invisible(self, bytype, identification, wait_time=120):
        by_type = get_by_type(bytype)

        ready = WebDriverWait(self.driver, wait_time).until_not(
            EC.visibility_of_all_elements_located((by_type, identification)))
        return ready

    def check_existence(self, bytype, identification):
        by_type = get_by_type(bytype)
        try:
            element = self.driver.find_element(by_type, identification)
            return True
        except NoSuchElementException:
            return False

    def check_existence_list(self, bytype, check_list):
        for item in check_list:
            if self.check_existence(bytype, item):
                return item
        return False

    def is_selected(self, bytype, identification, selection):
        by_type = get_by_type(bytype)
        self.wait_element_located(by_type, identification)
        select = Select(self.driver.find_element(by_type, identification))
        if select.first_selected_option.text == selection:
            return True
        else:
            return False

    def input_into(self, bytype, identification, content, clear=True):
        self.wait_element_located(bytype, identification)
        by_type = get_by_type(bytype)
        input_target = self.driver.find_element(by_type, identification)
        if clear:
            input_target.send_keys(Keys.CONTROL, 'a')
        input_target.send_keys(content)

    def open(self, link):
        self.driver.get(link)

    def select_by_text(self, bytype, identification, text):
        self.wait_element_located(bytype, identification)
        by_type = get_by_type(bytype)
        select = Select(self.driver.find_element(by_type, identification))
        select.select_by_visible_text(text)

    def submit(self, bytype, identification):
        self.wait_element_located(bytype, identification)
        by_type = get_by_type(bytype)
        submit_button = self.driver.find_element(by_type, identification)
        submit_button.submit()

    def click(self, bytype, identification):

        self.wait_element_clickable(bytype, identification)
        by_type = get_by_type(bytype)
        location = self.driver.find_element(by_type, identification)
        location.click()

    def element_enter(self, bytype, identification):
        self.wait_element_located(bytype, identification)
        by_type = get_by_type(bytype)
        element = self.driver.find_element(by_type, identification)
        element.send_keys(Keys.ENTER)

    def element_blank_space(self, bytype, identification):
        self.wait_element_located(bytype, identification)
        by_type = get_by_type(bytype)
        element = self.driver.find_element(by_type, identification)
        element.send_keys(Keys.SPACE)

    def upload_file(self, bytype, identification, location):
        self.wait_element_located(bytype, identification)
        by_type = get_by_type(bytype)
        field = self.driver.find_element(by_type, identification)
        field.send_keys(location)

    def get_text(self, bytype, identification):
        self.wait_element_located(bytype, identification)
        by_type = get_by_type(bytype)
        element = self.driver.find_element(by_type, identification)
        text = element.text
        return text

    def exec_script(self, script):
        self.driver.execute_script(script)

    def wait_page_fully_load(self, sleep_time=1):
        page_hash = 'empty'
        page_hash_new = ''

        while page_hash != page_hash_new:
            page_hash = self.get_page_hash()
            time.sleep(sleep_time)
            page_hash_new = self.get_page_hash()

    def get_page_hash(self):
        dom = self.driver.find_element(By.TAG_NAME, 'html').get_attribute('innerHTML')
        dom_hash = hash(dom.encode('utf-8'))
        return dom_hash

    def get_element_value(self, bytype, identification, selector):
        self.wait_element_located(bytype, identification)
        by_type = get_by_type(bytype)
        element = self.driver.find_element(by_type, identification)
        return element.get_attribute(selector)

    def is_current_url(self, url: str):
        return self.driver.current_url == url

    def quit(self):
        self.driver.quit()
