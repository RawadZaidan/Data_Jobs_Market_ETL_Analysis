from lookup import glassdoor, glassdoor_classes, glassdoor_xpaths,glassdoor_css_selectors, linkedin_url, linkedin_xpaths, linkedin_attributes, nakuri_url
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
#------------------------------------------------------------------------------------#
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
                glassdoor_wait()
            except:
                glassdoor_wait()
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

def glassdoor_get_id(x):
    id = x.split('=')[-1]
    return id

def glassdoor_cleaning_functions(df):
    df = df.applymap(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'N/A')
    df['posting_date'] = df['posting_date'].apply(glassdoor_return_time)
    df['company'] = df['company'].apply(glassdoor_clean_company_name)
    df['Yearly_Min'] = df['salary'].apply(glassdoor_return_yearly_lower)
    df['Yearly_Max'] = df['salary'].apply(glassdoor_return_yearly_higher)
    df['ID'] = df['link'].apply(glassdoor_get_id)
    return df

def glassdoor_get_all_postings_df(driver):
    data_list = []
    listings = glassdoor_get_elements_by_css(glassdoor_css_selectors.LI_JOBS_LIST.value, driver)
    for job in listings:
        titles, companies, locations, salaries, job_links, date = glassdoor_fetch_job_info(job)
        data = {'title': titles, 'company': companies, 'location': locations,
                'link': job_links, 'salary': salaries, 'posting_date': date}
        data_list.append(data)
    df = pd.DataFrame(data_list)
    return df

def glassdoor_final_df():

    driver = glassdoor_driver_goto_wait()
    glassdoor_scroll_to_bottom(driver)
    unclean_df = glassdoor_get_all_postings_df(driver)
    df = glassdoor_cleaning_functions(unclean_df)
    order = ['ID', 'title', 'company', 'location', 'posting_date', 'link']
    df = df[order]
    df['source'] = 'Glassdoor'

    return df
#------------------------------------------------------------------------------------#
# LinkedIn functions:

def linkedin_html_session():
    session = HTMLSession()
    return session

def linkedin_get_page(session, url=linkedin_url.url.value):
    page = session.get(url)
    return page

def linkedin_wait():
    sleep(randint(2,4))

def linkedin_return_all_elements_by_xpath(xpath, session, attr=False, attribute_name=None):
    items = session.html.xpath(xpath)
    if items:
        if attr:
            items_list = [item.attrs.get(attribute_name, 'N/A') for item in items]
        else:
            items_list = [item.text for item in items]
    else:
        items_list = 'N/A'
    
    return items_list

def linkedin_get_text_value(parent_element,css_selector):
    value = parent_element.find(css_selector)[0].text
    return value

def linkedin_job_id_extract(x):
    id = x.split('?refId')[0].split('-')[-1]
    id = int(id)
    return id

def linkedin_return_all_elements_as_df(page):

    titles = linkedin_return_all_elements_by_xpath(linkedin_xpaths.JOB_TITLE.value, page)
    companies = linkedin_return_all_elements_by_xpath(linkedin_xpaths.COMPANIES.value, page)
    locations = linkedin_return_all_elements_by_xpath(linkedin_xpaths.LOCATIONS.value, page)
    links = linkedin_return_all_elements_by_xpath(linkedin_xpaths.LINKS.value, page, attr=True, attribute_name=linkedin_attributes.HREF.value)
    times = linkedin_return_all_elements_by_xpath(linkedin_xpaths.POSTING_TIME.value, page, attr=True, attribute_name=linkedin_attributes.DATETIME.value)

    return titles, companies, locations, links, times

def linkedin_id_order(df):

    df['ID'] = df['link'].apply(linkedin_job_id_extract)
    order = ['ID', 'title', 'company', 'location', 'posting_date', 'link']
    df = df[order]
    df['source'] = 'LinkedIn'

    return df

def linkedin_fetch_df():
    session = HTMLSession()

    dff = pd.DataFrame()
    data_list = []
    countries = ['Worldwide','France', 'Germany', 'United%20Kingdom', 'United%20States', 'Canada']
    titles = [ 'Data%2Bengineer','Data%2Banalyst', 'Data%2Bscientist', 'BI%2Banalyst', 'etl%2Bdeveloper']
    for title in titles:
        for country in countries:
            for counter in range(0, 50 ,25):
                try:
                    url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={title}&location={country}'
                    url = url + f'&locationId=&f_TPR=r86400&start={counter}'
                    print('Now on page: ', counter)
                    page = linkedin_get_page(session, url=url)
                    # Use Requests-HTML functions to scrape data from the page
                    items = page.html.xpath('//li')
                    if len(items) == 0:
                        break
                    for li in items:
                        titles = li.find('h3')[0].text
                        companies = li.find('a.hidden-nested-link')[0].text
                        locations = li.find('span.job-search-card__location')[0].text
                        links = li.find('a.base-card__full-link')[0].attrs['href']
                        time = li.find('time')[0].attrs['datetime']

                        data = {'title': titles, 'company': companies, 'location': locations,
                                'link': links, 'posting_date': time}

                        data_list.append(data)

                    counter += 25
                except:
                    pass
                
    df = pd.DataFrame(data_list)
    dff = pd.concat([dff,df], ignore_index=True)
    return dff

def linkedin_final_df():

    df = linkedin_fetch_df()
    df = linkedin_id_order(df)

    return df

#------------------------------------------------------------------------------------#
# NakuriGulf functions 


def nakuri_driver():
    option= webdriver.ChromeOptions()
    option.add_argument('--incognito')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                         options=option)
    return driver

def nakuri_quit_driver(driver):
    driver.quit()

def nakuri_page_go_to(driver, url=nakuri_url.url.value):
    driver.get(url)

def nakuri_wait():
    sleep(randint(3, 6))

# def glassdoor_get_num_of_jobs(driver):
#     num_of_jobs = driver.find_element(By.XPATH,
#                                       glassdoor_xpaths.XPATH_NUMBER_OF_ELEMENTS.value).text
#     return num_of_jobs

def nakuri_get_text_values_by_class(class_name,driver):
    values_list=[]
    text_values = driver.find_elements(By.CLASS_NAME,class_name)
    for val in text_values:
        values_list.append(val.text)
    return values_list[0]

def nakuri_get_href_by_class(class_name,driver):
    values_list = []
    href_values = driver.find_elements(By.CLASS_NAME,class_name)
    for val in href_values:
        values_list.append(val.get_attribute('href'))
    return values_list[0]

def nakuri_get_elements_by_css(css_selector,driver, text=False):
    items = []
    elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
    if text==True:
        for el in elements:
            items.append(el.text)
        return items
    else:
        return elements

def nakuri_driver_goto_wait():
    driver = nakuri_driver()
    nakuri_page_go_to(driver)
    nakuri_wait()
    return driver

def nakuri_get_date(t):
    current_date = datetime.now()
    t = t.split(' ')
    if len(t)>2:
        t = t[-3:]
        if t[0] == 'on':
            day = int(t[1])
            month_name = t[2]
            month_dict = {
                'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
            }
            month = month_dict.get(month_name, 1)
            year = current_date.year
            date_o = str(day)+'-'+str(month)+'-'+str(year)
            return date_o

        elif t[2] == 'ago':
            days_ago = int(t[0])
            date_o = current_date - timedelta(days=days_ago)
            date_o = date_o.strftime("%d-%m-%Y")
            return date_o
    elif len(t) == 2:
        if t[-1] == 'Today':
            date_o = current_date.strftime("%d-%m-%Y")
            return date_o
        else:
            return 'ERROR'
        
def nakuri_get_time(job):
    time = nakuri_get_elements_by_css('span.time',job)[0].text
    clean_date = nakuri_get_date(time)
    return clean_date

def nakuri_location(job):
    location_ = nakuri_get_elements_by_css('li.info-loc', job)
    location = location_[0].text
    return location

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

def nakuri_fetch_job_info(driver):
    titles    = nakuri_get_text_values_by_class('designation-title',driver)
    companies = nakuri_get_text_values_by_class('info-org ',driver)
    locations = nakuri_location(driver)
    job_links = nakuri_get_href_by_class('info-position', driver)
    date      = nakuri_get_time(driver)
    return titles, companies, locations,  job_links, date

def glassdoor_scroll_to_bottom(driver):
    while True:
        try:
            try:
                glassdoor_wait()
                exit = glassdoor_find_exit_login_button(driver)
                glassdoor_click(exit)
                glassdoor_wait()
            except:
                glassdoor_wait()
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

def glassdoor_get_id(x):
    id = x.split('=')[-1]
    return id

def glassdoor_cleaning_functions(df):
    df = df.applymap(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'N/A')
    df['posting_date'] = df['posting_date'].apply(glassdoor_return_time)
    df['company'] = df['company'].apply(glassdoor_clean_company_name)
    df['Yearly_Min'] = df['salary'].apply(glassdoor_return_yearly_lower)
    df['Yearly_Max'] = df['salary'].apply(glassdoor_return_yearly_higher)
    df['ID'] = df['link'].apply(glassdoor_get_id)
    return df

def nakuri_get_all_postings_df(driver):
    data_list = []
    listings = nakuri_get_elements_by_css('div.ng-box.srp-tuple', driver)
    for job in listings:
        titles, companies, locations, job_links, date = nakuri_fetch_job_info(job)
        data = {'title': titles, 'company': companies, 'location': locations,
                'link': job_links, 'posting_date': date}
        data_list.append(data)
    df = pd.DataFrame(data_list)
    return df

def glassdoor_final_df():

    driver = glassdoor_driver_goto_wait()
    glassdoor_scroll_to_bottom(driver)
    unclean_df = glassdoor_get_all_postings_df(driver)
    df = glassdoor_cleaning_functions(unclean_df)
    order = ['ID', 'title', 'company', 'location', 'posting_date', 'link']
    df = df[order]
    df['source'] = 'Glassdoor'

    return df