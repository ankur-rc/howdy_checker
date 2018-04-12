
# coding: utf-8
# author: Ankur Roy Chowdhury

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class HowdyChecker():

    def __init__(self, howdy_site=None, output_file=None, chrome_driver_path='/usr/local/bin/chromedriver'):

        self.HOWDY_SITE = howdy_site
        self.OUTPUT_FILE = output_file
        opt = webdriver.chrome.options.Options()
        opt.set_headless()
        self.driver = webdriver.Chrome(
            executable_path=chrome_driver_path, options=opt)
        self.driver.implicitly_wait(30)
        # driver.maximize_window()

    def login(self, uname=None, passwd=None):

        self.driver.get(self.HOWDY_SITE)

        login_button = self.driver.find_element_by_id("loginbtn")
        login_button.click()

        username_field = self.driver.find_element_by_id('username')
        username_field.send_keys(uname)
        username_field.submit()

        password_field = self.driver.find_element_by_id('password')
        password_field.send_keys(passwd)
        password_field.submit()

    def check_course(self, term=None, subject=None, course=None):

        self.TERM = term
        self.SUBJECT = subject
        self.COURSE = course

        class_search_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="portlet_u31l1n51"]/div/span[1]/div/a')))

        class_search_link.click()

        # self.driver.switch_to.frame(0)
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, 'iframe')))

        select = Select(self.driver.find_element_by_id('term_input_id'))
        select.select_by_visible_text(self.TERM)

        self.driver.find_element_by_xpath(
            '/html/body/div[3]/form/input').submit()

        select = Select(self.driver.find_element_by_id('subj_id'))
        select.select_by_value(self.SUBJECT)

        self.driver.find_element_by_xpath(
            '//*[@id="courseBtnDiv"]/input[2]').click()

        course_view_btn = self.driver.find_elements_by_xpath(
            "//input[../../../td=" + self.COURSE + "]")

        course_view_btn[-1].click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@value='Register']")))

        course_sections = self.driver.find_elements_by_class_name('datadisplaytable')[
            0]

        course_content = course_sections.get_attribute('innerHTML')
        #print course_content

        return course_content

    def compare_contents(self, current_content=None):

        previous_contents = ''
        changed = False
        with open(self.OUTPUT_FILE, 'r') as f:
            previous_contents = f.read()

        if previous_contents == current_content:
            changed = False
        else:
            changed = True

        with open(self.OUTPUT_FILE, 'w') as f:
            f.write(current_content)

        return changed, current_content, previous_contents

    def __del__(self):
        self.driver.quit()
