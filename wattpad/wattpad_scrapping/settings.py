from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os



def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--log-level=3")  # Suppress console logs (INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver_path = os.path.join("wattpad_scrapping", "utils", "chromedriver-win64", "chromedriver-win64", "chromedriver.exe")
    
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver