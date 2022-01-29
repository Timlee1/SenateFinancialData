from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import numpy
import pandas as pd


def test():
    PATH = "C:/Users/15165/Documents/chromedriver.exe"
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(PATH, options=options)

    ROOT = "https://efdsearch.senate.gov"
    driver.get("https://efdsearch.senate.gov")
    SEARCH_PAGE = ROOT + '/search/'
    tokensoup = BeautifulSoup(driver.page_source, 'html.parser')
    print(tokensoup)


test()
