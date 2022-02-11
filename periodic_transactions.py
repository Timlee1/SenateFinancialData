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
import scraper

df = pd.read_csv('search_data.csv')

HOME = 'https://efdsearch.senate.gov'
wait = 2


def all_periodic_transactions():
    driver = user_agreement()
    time.sleep(wait)
    lst_all_pages = []
    # for ind in df.index:
    for ind in range(100):
        time.sleep(wait)
        s = df['Report Type'][ind]
        # if df['Report Type'][ind] == "Periodic Transaction Report":
        if s.find("Periodic Transaction Report") != -1:
            url = HOME + df['Report'][ind]
            fname = df['First'][ind]
            lname = df['Last'][ind]
            res = periodic_transactions(driver, url, fname, lname)
            lst_all_pages.append(res)

    flatten_lst = scraper.flatten_twod_list(lst_all_pages)
    df_to_csv(flatten_lst)


def remove_all_whitespace(str):
    str = str.replace("\n", "")
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
            row.append(td)
        res.append(row)
    return res


def df_to_csv(res):
    df = pd.DataFrame(res)
    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/test.csv',
              index=False, header=True)


def df_clean_to_csv(res):
    df = pd.DataFrame(res, columns=["First", "Last", "#", "Date", "Owner",
                                    "Ticker", "Asset Name", "Asset Type", "Type", "Amount", "Comment"])
    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/test.csv',
              index=False, header=True)


def data_clean_search(csv):
    df = pd.read_csv(csv)
    df.drop(['#', 'Owner', 'Comment'], axis=1, inplace=True)
    df['Ticker Link'] = df['Ticker']
    for ind in df.index:
        df['Date'][ind] = scraper.strip_td(df['Date'][ind]).strip()
        df['Ticker'][ind] = scraper.strip_td(df['Ticker'][ind]).strip()
        df['Asset Name'][ind] = scraper.strip_td(df['Asset Name'][ind]).strip()
        df['Asset Type'][ind] = scraper.strip_td(df['Asset Type'][ind]).strip()
        df['Type'][ind] = scraper.strip_td(df['Type'][ind]).strip()
        df['Amount'][ind] = scraper.strip_td(df['Amount'][ind]).strip()

        ticker_link, ticker = scraper.strip_ahref(df['Ticker'][ind])
        df['Ticker Link'][ind] = ticker_link
        df['Ticker'][ind] = ticker

    df = df.loc[df['Ticker'] != "-"]
    df = df.loc[df['Ticker'] != ""]
    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/test_clean.csv',
              index=False, header=True)

# periodic_transactions(user_agreement(
# ), 'https://efdsearch.senate.gov/search/view/ptr/a8e388bc-72c5-4227-b6f3-64b7bb779883/', "Doggy", "Cutie")


# all_periodic_transactions()
data_clean_search("test.csv")
