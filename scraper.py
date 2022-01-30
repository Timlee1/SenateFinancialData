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
    wait = 1
    PATH = "C:/Users/15165/Documents/chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    HOME = 'https://efdsearch.senate.gov'
    driver.get(HOME)

    token_element = driver.find_element(By.NAME, "csrfmiddlewaretoken")
    token = token_element.get_attribute('value')
    driver.find_element(By.XPATH, "//input[@id='agree_statement']").click()
    time.sleep(wait)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/fieldset[2]/div/div/div/div[1]/div/label/input").click()
    time.sleep(wait)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/fieldset[1]/div/div/div/div[1]/input").send_keys(fname)
    time.sleep(wait)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/fieldset[1]/div/div/div/div[2]/input").send_keys(lname)
    time.sleep(wait)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/div/button").click()
    time.sleep(wait)
    select = Select(driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[6]/div/div/div/div[3]/div[1]/div/label/select"))
    select.select_by_value('100')

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', attrs={'id': 'filedReports'})
    table_rows = table.find_all('tr', attrs={'class': ['odd', 'even']})

    res = []
    for tr in table_rows:
        row = []
        all_td = tr.find_all('td')
        for td in all_td:
            if td.find('a') != None:
                td = str(td.find('a'))
                start = td.find("=")
                end = td.find(">", start)
                sub = td[start+1:end]
                row.append(sub)
            else:
                td = str(td)
                start = td.find(">")
                end = td.find("<", start)
                sub = td[start+1:end]
                row.append(sub)
        res.append(row)

    df = pd.DataFrame(
        res, columns=["First", "Last", "Office", "Report", "Date"])
    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/data.csv',
              index=False, header=True)


scraper("Charles", "Schumer")
