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


def scraper():
    # Scape data from senate financial disclosures
    driver = main_to_search()
    wait = 3
    time.sleep(wait)
    html = driver.page_source
    lst_of_all_pages = []

    stop = True
    while(stop):
        lst_of_page = website_to_data(html)
        lst_of_all_pages.append(lst_of_page)
        try:
            driver.find_element(
                By.CSS_SELECTOR, ".paginate_button.next.disabled")
            stop = False
            break
        except:
            driver.find_element(
                By.CSS_SELECTOR, ".paginate_button.next").click()

    flatten_lst = []
    for nums in lst_of_all_pages:
        for val in nums:
            flatten_lst.append(val)
    df_to_csv(flatten_lst)


def main_to_search():
    # Go from user agreement to search page.
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
    return driver


def website_to_data(html):
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
    return res


def df_to_csv(list):
    df = pd.DataFrame(
        list, columns=["First", "Last", "Office", "Report", "Date"])
    df.to_csv(r'C:/Users/15165/Documents/Projects/SenateFinancialData/raw_search_data.csv',
              index=False, header=True)


scraper()
