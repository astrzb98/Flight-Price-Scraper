from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
from selenium.webdriver.common.by import By
import re
class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def do_click(self, by_locator):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(by_locator)).click()

    def do_send_keys(self, by_locator, text):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(by_locator)).send_keys(text)
        # self.driver.find_element(by_locator).send_keys(text)

    def get_element_text(self, by_locator):
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(by_locator)).text
        return element

    def switch_to_popup(self, frame_id):
        self.driver.switch_to.frame(frame_id)

    def switch_of_popup(self):
        self.driver.switch_to.default_content()

    def get_title(self, title):
        WebDriverWait(self.driver, 20).until(EC.title_is(title))
        return self.driver.title

    def is_visible(self, by_locator):
        element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(by_locator))
        return bool(element)

    def get_url(self):
        url = self.driver.current_url
        return url

    def redirect(self, url):
        self.driver.get(url)

    def get_elements_len(self, by_locator):
        condition_list = self.driver.find_elements(by_locator[0], by_locator[1])
        return len(condition_list)

    def set_inner_value(self, by_locator):
        self.driver.execute_script(by_locator)

    def perform_action_chain(self, by_locator):
        element = self.driver.find_element(by_locator[0], by_locator[1])
        actions = ActionChains(self.driver)
        actions.move_to_element(element).release().perform()

    def do_send_keys_label(self, by_locator, text):
        self.do_click(by_locator)
        self.do_send_keys(by_locator, text)

    def save_to_list(self,by_locator):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(by_locator))
        elements = self.driver.find_elements(by_locator[0],by_locator[1])
        scraped = [value.text for value in elements]
        return scraped

    def save_multi_to_single(self,by_locator):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(by_locator))
        elements = self.driver.find_elements(by_locator[0], by_locator[1])
        scraped = [value.text for value in elements]
        scrap_list = []
        for string in scraped:
            if "," in string:
                scrap_list.append("MultipleAirlines")
            else:
                string = re.sub(r"\s+", '', string)
                scrap_list.append(string)
        return scrap_list

    def check_exists_by_xpath(self,by_locator):
        while True:
            try:
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(by_locator)).click()
            except TimeoutException:
                break

