from lookup import glassdoor, glassdoor_classes, glassdoor_xpaths,glassdoor_css_selectors, linkedin_url
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from requests_html import HTMLSession
from selenium import webdriver
from random import randint
from time import sleep
import pandas as pd
import math
import time
import re 
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

def glassdoor_return_number_next_buttons(driver):
    nb_of_jobs = driver.find_element(By.XPATH,glassdoor_xpaths.XPATH_NUMBER_OF_ELEMENTS.value).text
    nb_of_jobs = int(nb_of_jobs.split()[0])
    skips = int(math.ceil(nb_of_jobs/20))-1
    return skips

def glassdoor_find_next_page_button(driver):
    nextpage = driver.find_element(By.XPATH,glassdoor_xpaths.XPATH_NEXT_PAGE.value)
    return nextpage

def glassdoor_find_exit_login_button(driver):
    exit = driver.find_element(By.XPATH,glassdoor_xpaths.XPATH_EXIT_LOGIN.value)
    return exit

def glassdoor_click(button_element):
    button_element.click()

def glassdoor_fetch_job_info(driver):
    titles    = glassdoor_get_text_values_by_class(glassdoor_classes.CLASS_JOB_TITLE.value, driver)
    companies = glassdoor_get_text_values_by_class(glassdoor_classes.CLASS_JOB_COMPANY_NAME.value, driver)
    locations = glassdoor_get_text_values_by_class(glassdoor_classes.CLASS_JOB_LOCATION.value, driver)
    salaries  = glassdoor_get_text_values_by_class(glassdoor_classes.CLASS_JOB_SALARY.value, driver)
    job_links = glassdoor_get_href_by_class(glassdoor_classes.CLASS_JOB_TITLE.value, driver)
    date      = glassdoor_get_elements_by_css(glassdoor_css_selectors.LI_JOB_DATE.value, driver, text=True)
    return titles, companies, locations, salaries, job_links, date

def glassdoor_scroll_to_bottom(driver):
    while True:
        try:
            try:
                glassdoor_wait()
                exit = glassdoor_find_exit_login_button(driver)
                glassdoor_click(exit)
            except:
                next = glassdoor_find_next_page_button(driver)
                glassdoor_click(next)
                glassdoor_wait()
        except:
            break
    print('Done scrolling pages')

def glassdoor_return_yearly_lower(l):

    m = l.split('(')
    m = m[0].split(' ')[:3]
    if m[0][-1].lower() == 'k':
        return m[0]
    elif m[0][-1].isdigit():
        try:
            price = int((float(m[0][1:])*40*4*12)/1000)
            m = '$'+str(price)+'K'
            return m
        except Exception as e:
            return 'ERROR'
    else:
        pass
def glassdoor_return_yearly_higher(l):

    m = l.split('(')
    m = m[0].split(' ')[:3]
    if m[0][-1].lower() == 'k':
        return m[-1]
    elif m[0][-1].isdigit():
        try:
            price = int((float(m[2][1:])*40*4*12)/1000)
            m = '$'+str(price)+'K'
            return m
        except Exception as e:
            return 'ERROR'
    else:
        pass

def glassdoor_cleaning_functions(df):
    df = df.applymap(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'N/A')
    df['date'] = df['date'].apply(glassdoor_return_time)
    df['company'] = df['company'].apply(glassdoor_clean_company_name)
    df['Yearly_Min'] = df['salary'].apply(glassdoor_return_yearly_lower)
    df['Yearly_Max'] = df['salary'].apply(glassdoor_return_yearly_higher)
    return df

def glassdoor_get_all_postings_df(driver):
    data_list = []
    listings = glassdoor_get_elements_by_css(glassdoor_css_selectors.LI_JOBS_LIST.value, driver)
    for job in listings:
        titles, companies, locations, salaries, job_links, date = glassdoor_fetch_job_info(job)
        data = {'title': titles, 'company': companies, 'location': locations,
                'link': job_links, 'salary': salaries, 'date': date}
        data_list.append(data)
    df = pd.DataFrame(data_list)
    return df

def glassdoor_final_df():

    driver = glassdoor_driver_goto_wait()
    glassdoor_scroll_to_bottom(driver)
    unclean_df = glassdoor_get_all_postings_df(driver)
    df = glassdoor_cleaning_functions(unclean_df)

    return df
#####################################################################################
# LinkedIn functions:

def linkedin_html_session():
    session = HTMLSession()
    return session

def linkedin_get_page(session, url=linkedin_url.url.value):
    page = session.get(url)
    return page

def linkedin_return_all_elements_by_xpath(xpath, session,attr=False,attribute_name=None):
    items_list = []
    items = session.html.xpath(xpath)
    if not attr:
        for item in items:
            items_list.append(item.text)
    elif attr:
        for item in items:
            items_list.append(item.attrs[attribute_name])
    return items_list

def return_all_elements_as_df():
    pass