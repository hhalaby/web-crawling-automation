import os.path
import random
import string
import time

import ait
import pyautogui
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

USERNAME = ''
PASSWORD = ''
URL = ''
SAVE_PATH = ''

COOKIES_BANNER_XPATH = ''
USERNAME_TEXTBOX_ID = ''
PASSWORD_TEXTBOX_ID = ''
LOGIN_BUTTON_ID = ''
BROWSE_BUTTON_1_ID = ''
SELECT_LIST_ID = ''
ITEMS_OF_INTEREST = []
SUB_ITEMS_OF_INTEREST = []

MATCHING_CSS_SELECTOR_FOR_SUB_ITEMS_OF_INTEREST = "[id*='POS_'"
MATCHING_CSS_SELECTOR_FOR_LIST_LEAVES = "[id*='LEAF_'"

SKIP_OVERWRITE_EXISTING = True


def wait():
    time.sleep(random.uniform(0.3, 0.6))


class Crawl:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("--disable-notifications")

        chrome_options.add_argument('--kiosk-printing')
        # chrome_options.add_argument('--disable-print-preview')

        # chrome_options.add_experimental_option('prefs', prefs)

        chrome_options.add_argument("--user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ("
                                    "KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52'")
        self.driver = webdriver.Chrome("chromedriver_v94.exe", options=chrome_options)
        # self.driver.maximize_window()
        self.vars = {}
        self.username = USERNAME
        self.password = PASSWORD
        self.url_login = URL
        self.items_of_interest = ITEMS_OF_INTEREST
        self.sub_items_of_interest = SUB_ITEMS_OF_INTEREST
        self.save_path = SAVE_PATH
        self.valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        # self.driver.execute_script("window.alert = function() {};")

    def teardown_method(self):
        self.driver.quit()
        self.driver.refresh()

    def login(self):
        self.driver.get(url=self.url_login)

        wait()
        self.driver.find_element(By.XPATH, COOKIES_BANNER_XPATH).click()

        wait()
        username = self.driver.find_element(By.ID, USERNAME_TEXTBOX_ID)
        username.send_keys(self.username)

        wait()
        password = self.driver.find_element(By.ID, PASSWORD_TEXTBOX_ID)
        password.send_keys(self.password)

        wait()
        self.driver.find_element(By.ID, LOGIN_BUTTON_ID).click()

    def print_asset(self):

        wait()
        self.driver.find_element(By.ID, BROWSE_BUTTON_1_ID).click()

        wait()
        select_list = Select(self.driver.find_element(By.ID, SELECT_LIST_ID))

        for item in self.items_of_interest:
            select_list.select_by_visible_text(item)

            wait()
            print("Clicking Sub-items")
            self.sub_items_list = self.driver.find_element(By.CSS_SELECTOR,
                                                           MATCHING_CSS_SELECTOR_FOR_SUB_ITEMS_OF_INTEREST)
            print(f'number of sub items 1st round: {len(self.sub_items_list)}')

            self.sub_items_already_clicked = []

            for sub_item in self.sub_items_list:
                if sub_item.text not in self.sub_items_of_interest:
                    self.sub_items_already_clicked.append(sub_item)
            print(f'number of clicked sub items 1st round: {len(self.sub_items_already_clicked)}')

            while len(self.sub_items_list) != len(self.sub_items_already_clicked):
                for sub_item in self.sub_items_list:
                    if sub_item not in self.sub_items_already_clicked:
                        # time.sleep(0.5)
                        attempts = 0
                        while attempts < 3:
                            try:
                                time.sleep(0.1)
                                sub_item.click()
                                break
                            except StaleElementReferenceException as e:
                                print(e)
                                print(f'Stale Element: {sub_item}')
                                time.sleep(0.1)
                            except ElementClickInterceptedException as e:
                                print(e)
                                time.sleep(0.1)
                            attempts += 1
                        self.sub_items_already_clicked.append(sub_item)
                time.sleep(0.1)
                self.sub_items_list = self.driver.find_element(By.CSS_SELECTOR,
                                                               MATCHING_CSS_SELECTOR_FOR_SUB_ITEMS_OF_INTEREST)
                print(f'# of sub items: {len(self.sub_items_list)}')
                print(f'# of clicked sub items: {len(self.sub_items_already_clicked)}')

            print("Finished clicking sub items")
            leaf_list = self.driver.find_element(By.CSS_SELECTOR, MATCHING_CSS_SELECTOR_FOR_LIST_LEAVES)
            print(f'number of leaves: {len(leaf_list)}')

            for leaf in leaf_list:

                time.sleep(0.5)
                attempts = 0
                while attempts < 3:
                    try:
                        leaf.click()
                        break
                    except ElementClickInterceptedException as e:
                        print(e)
                        time.sleep(0.1)
                    except UnexpectedAlertPresentException as e:
                        print(e)
                        break
                    except StaleElementReferenceException as e:
                        print(e)
                        print(f'Stale Element: {leaf}')
                    attempts += 1

                time.sleep(0.5)
                print(f'Getting name of leaf # {leaf_list.index(leaf)}')
                name = item + '_'
                try:
                    name += self.driver.find_element(By.ID, 'titleId').text
                except UnexpectedAlertPresentException as e:
                    print(e)
                    time.sleep(0.5)
                    ait.press('\n')
                    continue

                name = "".join(x for x in name if x in self.valid_chars)
                name.replace(' ', '_')
                path = self.save_path + name + '.pdf'
                # if item exists skip save
                if SKIP_OVERWRITE_EXISTING and os.path.isfile(path):
                    continue
                print(f'Printing leaf # {leaf_list.index(leaf)}')
                self.driver.find_element(By.CLASS_NAME, 'printbtn').click()
                time.sleep(0.1)
                attempts = 0
                while attempts < 3:
                    try:
                        self.driver.switch_to.window(test.driver.window_handles[1])
                    except IndexError as e:
                        print(e)
                    attempts += 1

                time.sleep(0.5)
                self.driver.execute_script('window.print();')

                time.sleep(0.5)
                pyautogui.typewrite(name)

                time.sleep(0.5)
                ait.press('\n')

                self.driver.close()
                time.sleep(0.2)
                self.driver.switch_to.window(test.driver.window_handles[0])


# start_time = time.time()
test = Crawl()
test.login()
test.print_asset()

# elapsed_time = (time.time() - start_time)/60
# print(f'{elapsed_time:.1f} minutes')
