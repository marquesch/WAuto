from services.util.tools.webdriverutil import DriverUtil, generate_xpath, get_by_type
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


class SagahDriverUtil(DriverUtil):
    def __init__(self):
        chrome_options = Options()
        prefs = {'safebrowsing.enabled': True}
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("prefs", prefs)
        exe_path = "chromedriver.exe"
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "normal"
        super(SagahDriverUtil, self).__init__(caps, chrome_options, exe_path)

    def check_disc_existence(self):
        disc_list = self.driver.find_elements(By.CSS_SELECTOR, '.list-item.d-flex.justify-space-between')
        return len(disc_list) > 0
