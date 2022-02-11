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

wait = 2


def scraper():
    # Scape all table data from senate financial disclosures
    driver = main_to_search()
    lst_of_all_pages = []
    time.sleep(wait)
    stop = True
    while(stop):
        html = driver.page_source
        lst_of_page = page_to_data(html)
        lst_of_all_pages.append(lst_of_page)
        time.sleep(wait)
        try:
            driver.find_element(
                By.CSS_SELECTOR, ".paginate_button.next.disabled")
            stop = False
            break
        except:
            driver.find_element(
                By.CSS_SELECTOR, ".paginate_button.next").click()
            time.sleep(wait)
    flatten_lst = flatten_twod_list(lst_of_all_pages)
    df_to_csv(flatten_lst)


def main_to_search():
    # Go from user agreement to search page.
    PATH = "C:/Users/15165/Documents/chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    HOME = 'https://efdsearch.senate.gov'
    driver.get(HOME)
    time.sleep(wait)
    driver.find_element(By.XPATH, "//input[@id='agree_statement']").click()
    time.sleep(wait)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/fieldset[2]/div/div/div/div[1]/div/label/input").click()
    time.sleep(wait)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/fieldset[1]/div/div/div/div[1]/input")
    time.sleep(wait)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/fieldset[1]/div/div/div/div[2]/input")
    time.sleep(wait)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[5]/div/form/div/button").click()
    time.sleep(wait)
    select = Select(driver.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div/div[6]/div/div/div/div[3]/div[1]/div/label/select"))
    select.select_by_value('100')
    time.sleep(wait)
    return driver


def page_to_data(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', attrs={'id': 'filedReports'})
    table_rows = table.find_all('tr', attrs={'class': ['odd', 'even']})
    res = []
    for tr in table_rows:
        row = []
        all_td = tr.find_all('td')
        for td in all_td:
            td = str(td)
            row.append(td)
        res.append(row)
    return res


def flatten_twod_list(lst):
    flatten_lst = []
    for rows in lst:
        for val in rows:
            flatten_lst.append(val)
    return flatten_lst


def df_to_csv(list):
    df = pd.DataFrame(
        list, columns=["First", "Last", "Office", "Report", "Date"])
    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/raw_data.csv',
              index=False, header=True)


def strip_td(s):
    start = s.find("<td>")
    end = s.find("</td>", start+4)
    return s[start+4:end]


def strip_ahref(s):
    start_link = s.find('"')
    end_link = s.find('"', start_link+1)
    link = s[start_link+1:end_link]
    start_type = s.find(">", end_link+1)
    end_type = s.find("<", start_type+1)
    link_type = s[start_type+1:end_type]
    return (link, link_type)


def data_clean_raw(csv):
    df = pd.read_csv(csv)
    df.drop(['Office'], axis=1, inplace=True)
    df['Report Type'] = df['Report']
    for ind in df.index:
        s = df['Report'][ind]
        if (s.find('paper') != -1) or (s.find('Amendment') != -1) or (s.find('Extension') != -1) or (s.find('Blind Trust') != -1) or (s.find('Candidate') != -1):
            df.drop(ind, inplace=True)
    for ind in df.index:
        df['First'][ind] = strip_td(df['First'][ind]).upper()
        space = df['First'][ind].find(" ")
        if space != -1:
            df['First'][ind] = df['First'][ind][:space]
        df['Last'][ind] = strip_td(df['Last'][ind]).upper()
        space = df['Last'][ind].find(" ")
        if space != -1:
            df['Last'][ind] = df['Last'][ind][:space]
        df['Date'][ind] = strip_td(df['Date'][ind])
        link, link_type = strip_ahref(df['Report'][ind])
        df['Report'][ind] = link
        df['Report Type'][ind] = link_type

    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/search_data.csv',
              index=False, header=True)


# scraper()
data_clean_raw('raw_data.csv')
