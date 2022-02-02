from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import json
import numpy as np
import pandas as pd
import time

#df = pd.read_csv('raw_data.csv')


def annual_reports(url):
    PATH = "C:/Users/15165/Documents/chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    HOME = 'https://efdsearch.senate.gov'
    driver.get(HOME)

    token_element = driver.find_element(By.NAME, "csrfmiddlewaretoken")
    token = token_element.get_attribute('value')
    driver.find_element(By.XPATH, "//input[@id='agree_statement']").click()
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    #html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    print(soup)


annual_reports(
    'https://efdsearch.senate.gov/search/view/annual/861b60bd-3808-4d4f-aa17-73d973ab21c9/')
