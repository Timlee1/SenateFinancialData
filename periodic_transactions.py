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
import data_cleaning

df = pd.read_csv('search_data.csv')
HOME = 'https://efdsearch.senate.gov'
wait = 3


def all_periodic_transactions():
    driver = user_agreement()
    time.sleep(wait)
    lst = []
    for ind in df.index:
        if df['Report Type'][ind] == "Periodic Transaction Report":
            url = HOME + df['Report'][ind]
            fname = df['First'][ind]
            lname = df['Last'][ind]
            res = periodic_transactions(driver, url, fname, lname)
            lst.append(res)


def remove_all_whitespace(str):
    str = str.replace("\n", " ")
    return str.replace(" ", "")


def user_agreement():
    PATH = "C:/Users/15165/Documents/chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get(HOME)
    token_element = driver.find_element(By.NAME, "csrfmiddlewaretoken")
    token = token_element.get_attribute('value')
    driver.find_element(By.XPATH, "//input[@id='agree_statement']").click()
    return driver


def periodic_transactions(driver, url, fname, lname):
    driver.get(url)
    time.sleep(wait)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table')
    table_rows = table.find_all('tr')
    res = []
    for i in range(1, len(table_rows)):
        tr = table_rows[i]
        row = []
        row.append(fname)
        row.append(lname)
        all_td = tr.find_all('td')
        for i in range(len(all_td)):
            td = all_td[i]
            td = str(td)
            if i == 3:
                td = remove_all_whitespace(td)
                start = td.find("https")
                end = td.find("target")-1
                td = td[start:end]
            elif i == 4:
                td = td.replace("\n", "")
                td = data_cleaning.strip_td(td).strip()
            else:
                td = remove_all_whitespace(td)
                td = data_cleaning.strip_td(td)
            row.append(td)
        res.append(row)
    return res


def df_csv(res):
    df = pd.DataFrame(res)
    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/test.csv',
              index=False, header=True)


periodic_transactions(user_agreement(
), 'https://efdsearch.senate.gov/search/view/ptr/a8e388bc-72c5-4227-b6f3-64b7bb779883/', "Doggy", "Cutie")
