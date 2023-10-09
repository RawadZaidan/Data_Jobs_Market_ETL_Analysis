from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from time import sleep
from random import randint
import re 
import math
from datetime import datetime, timedelta
from lookup import glassdoor, glassdoor_classes, glassdoor_xpaths,glassdoor_css_selectors
# from bs4 import BeautifulSoup
# from lxml import etree as et
# from csv import writer
# import pandas as pd
# import threading
# from concurrent.futures import ThreadPoolExecutor, wait
# import selenium
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException

# Glassdoor functions

def glassdoor_driver():
    option= webdriver.ChromeOptions()
    option.add_argument('--incognito')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                         options=option)
    return driver

def glassdoor_quit_driver(driver):
    driver.quit()

def glassdoor_page_go_to(driver, url=glassdoor.link.value):
    driver.get(url)

def glassdoor_wait():
    sleep(randint(2, 6))

def glassdoor_get_num_of_jobs(driver):
    num_of_jobs = driver.find_element(By.XPATH,
                                      glassdoor_xpaths.XPATH_NUMBER_OF_ELEMENTS.value).text
    return num_of_jobs

def glassdoor_get_text_values_by_class(class_name,driver):
    values_list=[]
    text_values = driver.find_elements(By.CLASS_NAME,class_name)
    for val in text_values:
        values_list.append(val.text)
    return values_list

def glassdoor_get_href_by_class(class_name,driver):
    values_list = []
    href_values = driver.find_elements(By.CLASS_NAME,class_name)
    for val in href_values:
        values_list.append(val.get_attribute('href'))
    return values_list

def glassdoor_get_elements_by_css(css_selector,driver, text=False):
    items = []
    elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
    if text==True:
        for el in elements:
            items.append(el.text)
        return items
    else:
        return elements

def glassdoor_driver_goto_wait():
    driver = glassdoor_driver()
    glassdoor_page_go_to(driver)
    glassdoor_wait()
    return driver

def glassdoor_return_time(job_date):
    date_of_job = None
    now = datetime.now()
    if job_date[-1:] == 'd':
        date_of_job = now - timedelta(days=int(job_date[:-1]))
    elif job_date[-1:] == 'h':
        date_of_job = now - timedelta(days=1)
    date_of_job = date_of_job.strftime("%d-%m-%Y")
    return date_of_job

def glassdoor_clean_company_name(name):
    result = re.split(r'(\d)', name, 1)
    result
    return result[0]

def glassdoor_fetch_job_info(driver):
    titles    = glassdoor_get_text_values_by_class(glassdoor_classes.CLASS_JOB_TITLE.value, driver)
    companies = glassdoor_get_text_values_by_class(glassdoor_classes.CLASS_JOB_COMPANY_NAME.value, driver)
    locations = glassdoor_get_text_values_by_class(glassdoor_classes.CLASS_JOB_LOCATION.value, driver)
    salaries  = glassdoor_get_text_values_by_class(glassdoor_classes.CLASS_JOB_SALARY.value, driver)
    job_links = glassdoor_get_href_by_class(glassdoor_classes.CLASS_JOB_TITLE.value, driver)
    date      = glassdoor_get_elements_by_css(glassdoor_css_selectors.LI_JOB_DATE.value, driver, text=True)
    return titles, companies, locations, salaries, job_links, date