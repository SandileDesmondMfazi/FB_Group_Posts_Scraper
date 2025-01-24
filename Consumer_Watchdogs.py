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
#chrome_options.add_argument('--headless') # If you want to see the browser comment out this entire line

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

# Locate the button with aria-label="Decline optional cookies" (Europe)
try:
    phone_input = browser.find_element(By.XPATH, '//*[@id="login_popup_cta_form"]/div/div[3]/div/div/div/label')
    phone_input.send_keys(Username)
    password_input = browser.find_element(By.XPATH, '//*[@id="login_popup_cta_form"]/div/div[4]/div/div/div/label')
    password_input.send_keys(Password)
    login_click = browser.find_element(By.XPATH, '//*[@id="login_popup_cta_form"]/div/div[5]/div')
    login_click.click()
    print("Logged In!")
    
except:
    print("Could not Login!")
    pass

browser.implicitly_wait(20)

#Scroll down to load all results
try:
    # Get the initial scroll position
    last_height = browser.execute_script("return document.body.scrollHeight")
    time.sleep(10)
    html_list = []

    Count = 0
    
    while True:
        browser.implicitly_wait(15)
        # Scroll down to the bottom of the page using JavaScript
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(15)

        # Get the new scroll position
        new_height = browser.execute_script("return document.body.scrollHeight")

        # Retrieve the HTML
        html = browser.page_source

        # Parse the HTML using lxml
        root = lxml.html.fromstring(html)

        # Find all post elements
        post_elements = root.cssselect('div.x9f619.x1n2onr6.x1ja2u2z.x1jx94hy.x1qpq9i9.xdney7k.xu5ydu1.xt3gfkd.xh8yej3.x6ikm8r.x10wlt62.xquyuld')

        # Append the HTML of each post element to the list
        for post_element in post_elements:
            html_list.append(lxml.html.tostring(post_element).decode('utf-8'))
        
        Count += 1

        # Check if we've reached the bottom
        if new_height == last_height:
            break
        
        # Update the scroll position
        last_height = new_height
        
        print(f"scrolled: {Count}s")
        
except Exception as e:
    print(f"An error occurred: {e}")
    
    
# Combine the HTMLs
full_html = '\n'.join(html_list)

# Use BeautifulSoup to parse the HTML
soup = BeautifulSoup(full_html, 'html.parser')

#Close the browser
browser.close()

# Find all the posts' html
Posts = soup.find_all('div', class_='x9f619 x1n2onr6 x1ja2u2z x1jx94hy x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld')

count = 0

for entry in Posts:
    count += 1

print(count)
# print(Name.prettify())

def parse_facebook_url(url):
  # Parse the URL
  parsed_url = 'https://www.facebook.com' + url.split('?')[0]
  return parsed_url

fb_Posts = []

for index, post in enumerate(Posts):
    PostID = index + 1
    Name = post.find('span', class_='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs')
    if Name:
        Author = Name.get_text(strip=True)
    else:
        Author = None 
    Post_Text = post.find('div', class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a')
    if Post_Text:
        Post_Content = Post_Text.get_text(strip=True)
    else:
        Post_Content = None 
    All_Reactions = post.find('span', class_='xt0b8zv x1jx94hy xrbpyxo xl423tq')
    if All_Reactions:
        No_of_Reacts = All_Reactions.get_text(strip=True)
    else:
        No_of_Reacts = None
    All_Comments = post.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xi81zsa')
    if All_Comments:
        No_of_Comments = All_Comments.get_text(strip=True)
    else:
        No_of_Comments = None

    TheComments = post.find_all('div', class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs")
    if TheComments:
        Comments = TheComments
    else:
        Comments = None

    if Comments is not None and len(Comments) > 0:
        Comment1 = Comments[0]
        First_Comment = Comment1.get_text()
        if len(Comments) > 1:
            Comment2 = Comments[1]
            Second_Comment = Comment2.get_text()
        else:
            Second_Comment = None
    else:
        First_Comment = None
        Second_Comment = None
    
    data = {
        # 'Post Id': PostID,
        'Author': Author,
        'Post Content': Post_Content,
        # 'Post Url': Post_Url
        'No of Reactions': No_of_Reacts,
        'No of Comments': No_of_Comments,
        'Comment One': First_Comment,
        'Comment Two': Second_Comment
    }
    fb_Posts.append(data)

Dataset = pd.DataFrame(fb_Posts)

Dataset

New_Data = Dataset.copy()

FB_Group_Data = New_Data.drop_duplicates(ignore_index=True)

FB_Group_Data = FB_Group_Data.dropna(subset=['Author'])

FB_Group_Data

FB_Group_Data.to_csv('Latest_Dataset_v3.csv', encoding='utf-8', index = True)