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


HOME = 'https://efdsearch.senate.gov'
wait = 2


def all_individual_reports(data_csv):
    df = pd.read_csv(data_csv)
    driver = scraper.main_to_search()
    time.sleep(wait)
    pt_lst_all_pages = []
    ar_lst_all_pages = []
    # for ind in df.index:
    for ind in range(50):
        time.sleep(wait)
        rpt_type = df['Report Type'][ind]
        """
        if rpt_type == "Periodic Transaction Report":
            url = HOME + df['Report'][ind]
            fname = df['First'][ind]
            lname = df['Last'][ind]
            res = periodic_transactions(driver, url, fname, lname)
            pt_lst_all_pages.append(res)
        """
        if rpt_type == "Annual Report":
            url = HOME + df['Report'][ind]
            fname = df['First'][ind]
            lname = df['Last'][ind]
            year = df['Date'][ind]
            res = annual_reports(driver, url, fname, lname, year)
            ar_lst_all_pages.append(res)
    """
    pt_flatten_lst = scraper.flatten_twod_list(pt_lst_all_pages)
    df_pt = pd.DataFrame(pt_flatten_lst, columns=["First", "Last", "#", "Date", "Owner",
                                                  "Ticker", "Asset Name", "Asset Type", "Type", "Amount", "Comment"])
    df_pt.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/periodic_transactions.csv',
                 index=False, header=True)
    """
    ar_flatten_lst = scraper.flatten_twod_list(ar_lst_all_pages)
    df_ar = pd.DataFrame(ar_flatten_lst, columns=["First", "Last", "Year", "#", "Asset", "Asset Type",
                                                  "Owner", "Value", "Income Type", "Income"])
    df_ar.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/annual_transactions.csv',
                 index=False, header=True)


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


def annual_reports(driver, url, fname, lname, year):
    driver.get(url)
    time.sleep(wait)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(
        "caption", text="List of assets added to this report").find_parent("table")
    table_rows = table.find_all('tr')
    res = []
    for i in range(1, len(table_rows)):
        tr = table_rows[i]
        row = []
        row.append(fname)
        row.append(lname)
        row.append(year)
        all_td = tr.find_all('td')
        for i in range(len(all_td)):
            td = all_td[i]
            td = str(td)
            row.append(td)
        res.append(row)
#    df = pd.DataFrame(res)
#    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/test.csv',
#              index=False, header=True)

    return res


def data_clean_pt(csv):
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

        if df['Asset Type'][ind] == "":
            df['Asset Type'][ind] = "Stock"
    df = df.loc[df['Ticker'] != "-"]
    df = df.loc[df['Ticker'] != ""]
    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/test_clean.csv',
              index=False, header=True)


def data_clean_ar(csv):
    df = pd.read_csv(csv)
    df.drop(['#', 'Owner', 'Income Type', 'Income'], axis=1, inplace=True)

    for ind in df.index:
        df['Asset'][ind] = scraper.strip_td(df['Asset'][ind]).strip()
        df['Asset Type'][ind] = scraper.strip_td(df['Asset Type'][ind]).strip()
        if df['Asset Type'][ind].find("div") != -1:
            df['Asset Type'][ind] = strip_div(df['Asset Type'][ind])
        df['Value'][ind] = scraper.strip_td(df['Value'][ind]).strip()
    df = df.loc[(df['Asset Type'] == "Stock") |
                (df['Asset Type'] == "Mutual Fund")]
    for ind in df.index:
        asset = df['Asset'][ind]
        asset = strip_strong(asset)
        if asset.find("a href") == -1:
            if asset[1].isUpper():
                ticker = ""
                name = asset[i+1:]
                for i in range(len(asset)):
                    if asset[i].isUpper():
                        ticker += asset[i]
                    else:
                        split = i
                        break
                link = ""
        else:
            pass
        df['Asset'][ind] = asset

    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/test_clean.csv',
              index=False, header=True)


def strip_div(s):
    start_find = s.find("div")
    start_txt = s.find(">", start_find)+1
    end_txt = s.find("</div>", start_txt)
    return s[start_txt:end_txt]


def strip_strong(s):
    start_find = s.find("strong")
    start_txt = s.find(">", start_find)
    end_txt = s.find("</strong>", start_txt)
    return s[start_txt+1:end_txt]


# all_individual_reports('search_data.csv')
# data_clean_pt("test.csv")
# annual_reports(scraper.main_to_search(
# ), 'https://efdsearch.senate.gov/search/view/annual/b2a6bec1-d597-4bd8-8d93-dc1235a1adea/', 'Doggy', 'Dog', 2019)
data_clean_ar("annual_transactions.csv")
