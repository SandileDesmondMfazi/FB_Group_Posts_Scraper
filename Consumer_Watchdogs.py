#Import Dependencies
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
from urllib.parse import urlparse
import json
import lxml.html

#Configure Chromedriver

chrome_install = ChromeDriverManager().install()

folder = os.path.dirname(chrome_install)
chromedriver_path = os.path.join(folder, "chromedriver.exe")

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument('--headless') # If you want to see the browser comment out this entire line

# Initialize Chrome WebDriver
browser = webdriver.Chrome(
    service = Service(chromedriver_path),
    options = chrome_options
)

with open('Config_file.json') as f:
    config = json.load(f)


#Setup search parameters
Username = config['facebook']['username']
Password = config['facebook']['password']


# Set up base URL
url = f'https://www.facebook.com/groups/ConsumerWatchdogBW'

# Visit the website
browser.get(url)