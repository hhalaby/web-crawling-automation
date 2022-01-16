import time
import winsound

# from pushsafer import init, Client
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

APPOINTMENT_URL = ''


class CheckAppointment:
    def setup_method(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path='chromedriver_v97.exe', options=chrome_options)
        self.vars = {}

    def teardown_method(self):
        self.driver.quit()

    def check_if_appointment_available(self):

        start_time = time.time()
        self.driver.get("APPOINTMENT_URL")
        try:
            self.driver.find_element(By.LINK_TEXT, "Accept").click()
        except NoSuchElementException:
            print('no cookies banner')
        self.driver.find_element(By.ID, "condition").click()
        time.sleep(0.2)
        self.driver.find_element(By.NAME, "nextButton").click()
        elements = self.driver.find_elements(By.NAME, "nextButton")
        # assert len(elements) == 0
        if len(elements) == 1:
            duration = 500  # milliseconds
            freq = 800  # Hz
            winsound.Beep(freq, duration)
            winsound.Beep(freq, duration)
            winsound.Beep(freq, duration)
            self.driver.save_screenshot("screenshot.png")
            image = Image.open('screenshot.png')
            image.show()
        else:
            print('Pas de RDV')
            self.driver.save_screenshot("screenshot.png")
            image = Image.open('screenshot.png')
            image.show()
            duration = 250  # milliseconds
            freq = 400  # Hz
            winsound.Beep(freq, duration)

            self.driver.quit()

        print("--- %s seconds ---" % (time.time() - start_time))
