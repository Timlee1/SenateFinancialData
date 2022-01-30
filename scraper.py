from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import json
import time
import numpy as np
import pandas as pd


def scraper(fname, lname):
    PATH = "C:/Users/15165/Documents/chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    HOME = 'https://efdsearch.senate.gov'
    driver.get(HOME)
    driver.implicitly_wait(3)

    token_element = driver.find_element(By.NAME, "csrfmiddlewaretoken")
    token = token_element.get_attribute('value')
    driver.find_element(By.XPATH, "//input[@id='agree_statement']").click()
    cookies = driver.get_cookies()
    print(cookies)
    driver.implicitly_wait(60)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/fieldset[2]/div/div/div/div[1]/div/label/input").click()

    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/fieldset[1]/div/div/div/div[1]/input").send_keys(fname)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/fieldset[1]/div/div/div/div[2]/input").send_keys(lname)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/div/button").click()

    select = Select(driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[6]/div/div/div/div[3]/div[1]/div/label/select"))
    select.select_by_value('100')
    time.sleep(10)


scraper("Charles", "Schumer")
