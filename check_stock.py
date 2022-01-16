import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import html_stripper

BASE_PRODUCT_PAGES = False

if BASE_PRODUCT_PAGES:
    url_to_get = ''
else:
    url_to_get = 'Specific stock api request URL'


class CheckStock:
    def setup_method(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome("chromedriver_v97.exe", options=chrome_options)
        self.driver.maximize_window()

    def teardown_method(self):
        self.driver.quit()

    def check_stock(self):
        self.driver.get(url_to_get)

        if BASE_PRODUCT_PAGES:
            # THE FOLLOWING CODE SHOULD BE USED IF ACCESSING A PRODUCT PAGE.
            self.driver.refresh()

            self.driver.find_element(By.ID, "didomi-notice-agree-button").click()

            self.driver.find_element(By.ID, "//*[@id='app']/main/article/div[1]/div[4]/div/button").click()
            self.driver.implicitly_wait(0.2)
            size_m_details = self.driver.find_element(By.ID, "option-product-size-selection-1")

            if len(size_m_details.find_elements_by_class_name("no")) > 0:
                print("Stock Available")
                return False
            else:
                print("NO STOCK")
                return True
        else:
            stock_dict = json.loads(html_stripper.strip_tags(self.driver.page_source))
            return stock_dict


test = CheckStock()
test.setup_method()
stock = test.check_stock()
