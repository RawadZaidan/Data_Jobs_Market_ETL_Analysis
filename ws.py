from lookup import glassdoor, glassdoor_classes, glassdoor_xpaths,glassdoor_css_selectors, linkedin_url, linkedin_xpaths, linkedin_attributes, nakuri_url
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from logging_handler import show_error_message
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from lookup import nakuri_get_info
from lookup import ErrorHandling
from selenium import webdriver
from random import randint
from time import sleep
import pandas as pd
import requests
import pickle
import math
import time
import re 
#-------------------------------------------------------------#
# Linkedin postings functions

def linkedin_html_session():
    session = HTMLSession()
    return session

# Waiting function for linkedin
def linkedin_wait():
    sleep(randint(2,4))

def linkedin_get_page(session, url=linkedin_url.url.value):
    page = session.get(url)
    return page

def linkedin_fetch_df():
    
    session = linkedin_html_session()

    dff = pd.DataFrame()
    data_list = []
    countries = ['United%20Kingdom', 'United%20States', 'Canada', 'Australia', 'UAE']
    titles = ['Data%2Bengineer','Data%2Banalyst', 'Data%2Bscientist', 'BI%2Banalyst', 'etl%2Bdeveloper']
    for title in titles:
        for country in countries:
            for counter in range(0, 225 ,25):
                try:
                    url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={title}&location={country}'
                    url = url + f'&locationId=&f_TPR=r86400&start={counter}'
                    # Use this if you want to see the pages you're on in the linkedin iterator
                    # print('Now on page: ', counter)
                    page = linkedin_get_page(session, url=url)
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

def linkedin_job_id_extract(x):
    id = x.split('?refId')[0].split('-')[-1]
    id = int(id)
    return id

def linkedin_id_order(df):

    df['ID'] = df['link'].apply(linkedin_job_id_extract)
    order = ['ID', 'title', 'company', 'location', 'posting_date', 'link']
    df = df[order]
    df['source'] = 'LinkedIn'
    df.drop_duplicates(subset='ID')
    return df

def linkedin_final_df():
    df = linkedin_fetch_df()
    df = linkedin_id_order(df)
    return df

#------------------------------------------------------------------------------------#
# LinkedIn Individual jobs functions 

def find_technologies_in_string(input_string):
    try:
        input_string = input_string.lower()
        techs = ["python", "sql", "r", "scala", "tableau", "power_bi", "mysql", "postgresql", "nosql", "etl", "dax", "aws", "azure","remote","hybrid","on_site","junior", "mid", "senior"]
        tech_found = {tech: tech in input_string for tech in techs}
        return tech_found
    except:
        tech_found = {tech: False for tech in techs}
        return tech_found

#This function takes a description blob and returns a salary list 
def linkedin_get_salary(description):
    cleaned_numbers = []
    try:
        start_euro = description.find('£')
        start_dollar = description.find(r'$')
        
        if start_euro != -1 and (start_dollar == -1 or start_euro < start_dollar):
            currency_symbol = '£'
            start = start_euro
        elif start_dollar != -1:
            currency_symbol = r'$'
            start = start_dollar
        else:
            return cleaned_numbers

        salary = description[start:start+40]
        pattern = r'\d{1,3}(?:,\d{3})*(?:\.\d+)?'
        numbers = re.findall(pattern, salary)
        cleaned_numbers = [float(num.replace(',', '')) for num in numbers]
        if currency_symbol == '£':
            cleaned_numbers = [1.22*num for num in cleaned_numbers]
    except:
        return cleaned_numbers
    return cleaned_numbers

#This function takes the previous postings df and iterates over each posting
# and fetches the relvant data

def linkedin_individual_iterate_and_get_df(df):
    try:
        data_list = []
        for i in range(len(df)):
            print(i,"/",len(df))
            try:
                SOURCE = 'LinkedIn'
                ID = df.iloc[i,0]
                url = df.iloc[i,-2]
                company_id = id_from_company_name(df.iloc[i,2])
                company_name = df.iloc[i,2]
                r = requests.get(url)
                s = bs(r.text, 'html.parser')
                digest = s.text
                job_description = s.find_all('div',class_="show-more-less-html__markup")[0].text
                sleep(randint(1,2))
                salary = linkedin_get_salary(digest)
                if len(salary)>1:
                    lower = salary[0]
                    higher = salary[1]
                elif len(salary) == 1:
                    lower = salary[0]
                    higher = salary[0]
                else:
                    lower = None
                    higher = None
                techs = find_technologies_in_string(digest)
                # data
                link = s.find_all("a", attrs={"data-tracking-control-name":"public_jobs_topcard_logo"})[0]
                link = link.get("href")
                data = {'ID':ID, 'source':SOURCE,'company_name':company_name,'company_id':company_id, 'min_yearly_salary':lower,
                            'max_yearly_salary':higher,'company_link':link,'description':job_description}
                data.update(techs)
                data_list.append(data)
                print('appended data')
            except:
                pass
        df_new = pd.DataFrame(data_list)
        return df_new
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.LINKEDIN_INDIVIDUAL_JOBS_ERROR.value
        show_error_message(error_prefix, suffix)
#----------------------------------------------------------------------#
# Linkedin Companies functions 

def id_from_company_name(company_name):
    try:
        #To return a unique, positive company identifier, 
        #we do modulus of a very large number so that we always get a positive number 
        return hash(company_name)% (2**31)
    except:
        return 'N/A'

# Takes a df from job details and iterates to get the company info
def linkedin_get_company_info(df_co):   
    try:
        data_list = []
        session = HTMLSession()
        df_co = df_co.drop_duplicates(subset='company_id')
        for i in range(len(df_co)):
            try:
                print(i,'/',len(df_co))
                company_id = df_co.iloc[i,3]
                url = df_co.iloc[i,6]
                company_name = df_co.iloc[i,2]
                r = session.get(url)
                sleep(2)
                ritems = r.html.xpath('//dd')
                company_direct_link = ritems[0].text
                industry = ritems[1].text
                size = ritems[2].text
                data = {'company_id':company_id,  'company_name':company_name,
                            'industry':industry,'size':size, 'direct_link':company_direct_link}
                data_list.append(data)
                print('appended data')
            except:
                pass
        df_new = pd.DataFrame(data_list)
        return df_new
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.LINKEDIN_COMPANY_INFO_ERROR.value
        show_error_message(error_prefix, suffix)

#----------------------------------------------------------------------#
# Naukri Functions use selenium
def selenium_driver():
    try:
        option= webdriver.ChromeOptions()
        option.add_argument('--incognito')
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                            options=option)
        return driver
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.SELENIUM_DRIVER_ERROR.value
        show_error_message(error_prefix, suffix)

def selenium_get_url(driver, url):
    try:
        driver.get(url)
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.SELENIUM_GET_ERROR.value
        show_error_message(error_prefix, suffix)

def quit_driver(driver):
    try:
        driver.quit()
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.QUIT_DRIVER_ERROR.value
        show_error_message(error_prefix, suffix)

def nakuri_get_text_values_by_class(class_name,driver):
    values_list=[]
    text_values = driver.find_elements(By.CLASS_NAME,class_name)
    for val in text_values:
        values_list.append(val.text)
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

def nakuri_get_href_by_class(class_name,driver):
    values_list = []
    href_values = driver.find_elements(By.CLASS_NAME,class_name)
    for val in href_values:
        values_list.append(val.get_attribute('href'))
    return values_list[0]

def nakuri_get_href_by_css(css_selector,driver, href=False):
    items = []
    elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
    if href==True:
        for el in elements:
            items.append(el.get_attribute('href'))
        return items
    else:
        return elements

def nakuri_get_job_description(driver):
    try:
        items = nakuri_get_elements_by_css('article.job-description', driver,text=True)
        desc = " ".join(items)
        return desc
    except:
        desc=None
        return desc

def wait():
    sleep(randint(3, 6))

def nakuri_get_date(t):
    try:
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
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.NAKURI_GET_DATE_ERROR.value
        show_error_message(error_prefix, suffix)
        
def nakuri_get_time(job):
    try:
        time = nakuri_get_elements_by_css('span.time',job)[0].text
        clean_date = nakuri_get_date(time)
        return clean_date
    except:
        return 'N/A'

def nakuri_location(job):
    try:
        location_ = nakuri_get_elements_by_css('li.info-loc', job)
        location = location_[0].text
        return location
    except:
        return 'N/A'

def nak_get_element_by_class(driver, class_name):
    try:
        element = driver.find_element(By.CLASS_NAME,class_name ).text
        return element
    except:
        return 'N/A'

def nak_get_links(driver):
    try:
        title = driver.find_element(By.CLASS_NAME, 'info-position').get_attribute('href')
        return title
    except:
        return 'N/A'

def nakuri_fetch_job_info(driver):
    try:
        titles    = nak_get_element_by_class(driver,nakuri_get_info.title.value)
        companies = nak_get_element_by_class(driver,nakuri_get_info.company.value)
        locations = nakuri_location(driver)
        job_links = nak_get_links(driver)
        date      = nakuri_get_time(driver)
        return titles, companies, locations,  job_links, date
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.NAKURI_GET_JOBS_ERROR.value
        show_error_message(error_prefix, suffix)

def nakuri_get_id(df):
    try:
        df['ID'] = df['link'].apply(lambda x: x.split('jid-')[-1])
        return df
    except Exception as error:  
        suffix = str(error)
        error_prefix = ErrorHandling.NAKURI_ID_ERROR.value
        show_error_message(error_prefix, suffix)

def nakuri_get_all_postings_df(driver):
    try:
        data_list = []
        listings = nakuri_get_elements_by_css('div.ng-box.srp-tuple', driver)
        for job in listings:
            titles, companies, locations, job_links, date = nakuri_fetch_job_info(job)
            data = {'title': titles, 'company': companies, 'location': locations,
                    'link': job_links, 'posting_date': date}
            data_list.append(data)
        df = pd.DataFrame(data_list)
        df['ID'] = df['link'].apply(lambda x: x.split('jid-')[-1])
        order = ['ID', 'title', 'company', 'location', 'posting_date', 'link']
        df = df[order]
        df['source'] = 'NakuriGulf'
        return df
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.NAKURI_GET_ALL_POSTINGS_ONEPAGE_ERROR.value
        show_error_message(error_prefix, suffix)

def nakuri_get_all_postings(driver):
    try:
        df = pd.DataFrame()
        for page in range(1,4):
            url = f"https://www.naukrigulf.com/data-engineer-jobs-{page}?sort=date"
            try:
                selenium_get_url(driver, url)
                sleep(5)
                dff = nakuri_get_all_postings_df(driver)
                df = pd.concat([df,dff], ignore_index=True)
            except:
                pass
        return df
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.NAKURI_GET_ALL_POSTINGS_ERROR.value
        show_error_message(error_prefix, suffix)
    
def nakuri_get_salary(salary):
    try: 
        pattern = r'(\d{1,3}(?:,\d{3})*)(?:\s*-\s*)(\d{1,3}(?:,\d{3})*)'

        match = re.search(pattern, salary)
        if match:
            lower = int(int(match.group(1).replace(',', ''))*0.27*12)
            higher = int(int(match.group(2).replace(',', ''))*0.27*12)
        else:
            lower,higher = 'N/A', 'N/A'
        return lower,higher
    except:
        return 'N/A', 'N/A'

def nakuri_get_salary_final(driver):
    try:
        elements = driver.find_elements(By.CSS_SELECTOR,'p.value')
        for el in elements:
            if el.text[0:3] == 'AED':
                salary = el.text
        lower,higher = nakuri_get_salary(salary)
    except:
        salary = 'N/A'
        lower,higher = 'N/A', 'N/A'
    finally:
        return lower, higher

def nakuri_get_techs(digest_string) -> dict:
    try:
        techs = find_technologies_in_string(digest_string)
        return techs
    except:
        return find_technologies_in_string('Sample')

def nakuri_get_job_details(df,driver):
    try:
        data_list = []
        try:
            for i in range(len(df)):
                print('Doing: ',i+1,'/',len(df))
                ID = df.iloc[i,0]
                SOURCE = df.iloc[i, -1]
                url = df.iloc[i,5]
                company_name = df.iloc[i,2]
                company_id   = id_from_company_name(company_name)
                selenium_get_url(driver, url)
                sleep(2)
                company_link = 'N/A'
                lower, higher = nakuri_get_salary_final(driver)
                digest = driver.find_elements(By.CLASS_NAME, 'job-description')
                digestion = ''
                for line in digest:
                    digestion+= line.text
                techs = nakuri_get_techs(digestion)
                data = {'ID':ID, 'source':SOURCE,'company_name':company_name,
                        'company_id':company_id, 'min_yearly_salary':lower,
                        'max_yearly_salary':higher,'company_link':company_link,
                        'description':digestion}
                data.update(techs)
                data_list.append(data)
        except:
            pass
        df_ind = pd.DataFrame(data_list)
        return df_ind
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.NAKURI_GET_DETAILS_ERROR.value
        show_error_message(error_prefix, suffix)
#-------------------------------------------------------------#
# Glassdoor functions 

def glassdoor_quit_driver(driver):
    driver.quit()

def glassdoor_wait():
    sleep(randint(2, 6))

def glassdoor_get_num_of_jobs(driver):
    num_of_jobs = driver.find_element(By.XPATH,
                                      glassdoor_xpaths.XPATH_NUMBER_OF_ELEMENTS.value).text
    return num_of_jobs

def glassdoor_get_text_values_by_class(class_name,driver):
    values_list=None
    try:
        text_values = driver.find_element(By.CLASS_NAME,class_name)
        values_list = text_values.text
    except:
        values_list=None
    return values_list

def glassdoor_get_text_by_class(driver, class_name):
    try:
        values = driver.find_elements(By.CLASS_NAME,class_name)
        if len(values):
            return values[0].text
    except:
        return 'N/A'

def glassdoor_get_href_by_class(class_name,driver):
    values_list = []
    href_values = driver.find_elements(By.CLASS_NAME,class_name)
    for val in href_values:
        values_list.append(val.get_attribute('href'))
    return values_list

def glassdoor_get_href_values_by_css(driver,css='a.link'):
    values_list=[]
    text_values = driver.find_elements(By.CSS_SELECTOR,css)
    for val in text_values:
        values_list.append(val.get_attribute('href'))
    return values_list

def glassdoor_get_elements_by_css(css_selector,driver,text=False):
    items = []
    elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
    if text==True:
        for el in elements:
            items.append(el.text)
        return items
    else:
        return elements

def glassdoor_driver_goto_wait():
    driver = selenium_driver()
    selenium_get_url(driver, url=glassdoor.link.value)
    glassdoor_wait()
    return driver

def glassdoor_return_time(job_date):
    date_of_job = None
    try:
        now = datetime.now()
        if job_date[-1:] == 'd':
            date_of_job = now - timedelta(days=int(job_date[:-1]))
        elif job_date[-1:] == 'h':
            date_of_job = now - timedelta(days=1)
        date_of_job = date_of_job.strftime("%d-%m-%Y")
    except:
        return date_of_job
    return date_of_job

def glassdoor_clean_company_name(name):
    if name:
        result = re.split(r'(\d)', str(name), 1)
        results =result[0].replace('\n', '')
        return results
    else:
        return 'None'

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

def glassdoor_find_company_button(driver):
    company_page = driver.find_element(By.XPATH,'//*[@id="PageContent"]/div[1]/div[2]/header/div/div/div[3]/span')
    return company_page

def glassdoor_fetch_job_info(job):
    titles    = glassdoor_get_text_by_class(job,glassdoor_classes.CLASS_JOB_TITLE.value)
    companies = glassdoor_get_text_by_class(job, glassdoor_classes.CLASS_JOB_COMPANY_NAME.value)
    locations = glassdoor_get_text_by_class(job, glassdoor_classes.CLASS_JOB_LOCATION.value)
    salaries  = glassdoor_get_text_by_class(job, glassdoor_classes.CLASS_JOB_SALARY.value)
    job_links = glassdoor_get_href_by_class(glassdoor_classes.CLASS_JOB_TITLE.value, job)
    date      = glassdoor_get_elements_by_css(glassdoor_css_selectors.LI_JOB_DATE.value, job, text=True)
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
    try:
        m = l.split('(')
        m = m[0].split(' ')[:3]
        if m[0][-1].lower() == 'k':
            return int(m[0][1:-1])*1000
        elif m[0][-1].isdigit():
            try:
                price = int((float(m[0][1:])*40*4*12)/1000)
                m = '$'+str(price)+'K'
                return m
            except Exception as e:
                return 'ERROR'
        else:
            pass
    except:
        return 'N/A'

def glassdoor_return_yearly_higher(l):
    try:
        m = l.split('(')
        m = m[0].split(' ')[:3]
        if m[0][-1].lower() == 'k':
            return int(m[-1][1:-1])*1000
        elif m[0][-1].isdigit():
            try:
                price = int((float(m[2][1:])*40*4*12)/1000)
                m = '$'+str(price)+'K'
                return m
            except Exception as e:
                return 'ERROR'
        else:
            pass
    except:
        return 'N/A'

def glassdoor_get_id(x):
    try:
        id = x.split('=')[-1]
        return id
    except:
        return 'N/A'

def glassdoor_cleaning_functions(df):
    try:
        df['posting_date'] = df['posting_date'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'N/A')
        df['link'] = df['link'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'N/A')
        df['posting_date'] = df['posting_date'].apply(glassdoor_return_time)
        df['posting_date'] = df['posting_date'].apply(lambda x: x.replace('-', '/'))
        df['company'] = df['company'].apply(glassdoor_clean_company_name)
        df['ID'] = df['link'].apply(glassdoor_get_id)
        return df
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.GLASSDOOR_CLEANING_POSTINGS_ERROR.value
        show_error_message(error_prefix, suffix)

def glassdoor_get_all_postings_df(driver):
    try:
        data_list = []
        listings = glassdoor_get_elements_by_css(glassdoor_css_selectors.LI_JOBS_LIST.value, driver)
        for job in listings:
            titles, companies, locations, salaries, job_links, date = glassdoor_fetch_job_info(job)
            data = {'title': titles, 'company': companies, 'location': locations,
                    'link': job_links, 'salary': salaries, 'posting_date': date}
            data_list.append(data)
        df = pd.DataFrame(data_list)
        return df
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.GLASSDOOR_FETCH_POSTINGS_ERROR.value
        show_error_message(error_prefix, suffix)

def glassdoor_final_df(driver):
    try:
        selenium_get_url(driver, url=glassdoor.link.value)
        sleep(5)
        glassdoor_scroll_to_bottom(driver)
        df = glassdoor_get_all_postings_df(driver)
        df = df[df['title'].notna()]
        df = glassdoor_cleaning_functions(df)
        order = ['ID', 'title', 'company', 'location', 'posting_date', 'link']
        df = df[order]
        df['source'] = 'Glassdoor'
        return df
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.GLASSDOOR_POSTINGS_ERROR.value
        show_error_message(error_prefix, suffix)
#-------------------------------------------------#
# Glassdoor individual jobs functions 

def glassdoor_get_href_by_xpath(driver,xpath):
    try:
        company_link = driver.find_element(By.XPATH, xpath).get_attribute('href')
        return company_link
    except:
        return 'N/A'

def glassdoor_get_elements_by_css_selector(driver,css_selector):
    try:
        digest = driver.find_element(By.CSS_SELECTOR, css_selector).text
        return digest
    except:
        return 'N/A'

from lookup import glassdoor_xpaths

# Takes first listings df
def glassdoor_ind_jobs_df(driver,df):
    try:
        data_list = []
        for i in range(len(df)):
            print('Doing: ',i,'/',len(df))
            ID = df.iloc[i,0]
            SOURCE = df.iloc[i, -1]
            url = df.iloc[i,5]
            selenium_get_url(driver, url=url)
            company_name = glassdoor_find_element_by_xpath(driver,glassdoor_xpaths.XPATH_COMP_NAME.value)
            company_id = id_from_company_name(company_name)
            company_link = glassdoor_get_href_by_xpath(driver,glassdoor_xpaths.XPATH_COMP_LINK.value)
            salary = glassdoor_find_element_by_xpath(driver,glassdoor_xpaths.XPATH_SALARY.value)
            lower = glassdoor_return_yearly_lower(salary)
            higher = glassdoor_return_yearly_higher(salary)
            digest = glassdoor_get_elements_by_css_selector(driver,'div.desc')
            techs = find_technologies_in_string(digest)
            data = {'ID':ID, 'source':SOURCE,'company_name':company_name,'company_id':company_id, 'min_yearly_salary':lower,
                        'max_yearly_salary':higher,'company_link':company_link,'description':digest}
            data.update(techs)
            data_list.append(data)
        df_ind = pd.DataFrame(data_list)
        return df_ind
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.GLASSDOOR_INDIVIDUALS_ERROR.value
        show_error_message(error_prefix, suffix)

#--------------------------------------------------------------------#
# Glassdoor companies functions 

def glassdoor_find_element_by_xpath(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath).text
        return element
    except:
        return 'N/A'

def glassdoor_companies_info_df(driver, df_ind):
    try:
        df = df_ind.drop_duplicates(subset='company_id')
        data_list = []
        for i in range(len(df)):
            print('Doing: ',i+1,'/',len(df))
            Comp_ID      = df.iloc[i,0]
            url          = df.iloc[i,6]
            company_name = df.iloc[i,2]
            selenium_get_url(driver, url)
            sleep(3)
            industry     = glassdoor_find_element_by_xpath(driver, '//*[@id="MainContent"]/div[1]/div/ul/li[8]/a')
            size         = glassdoor_find_element_by_xpath(driver, '//*[@id="MainContent"]/div[1]/div/ul/li[3]')
            direct_link  = glassdoor_find_element_by_xpath(driver, '//*[@id="MainContent"]/div[1]/div/ul/li[1]/a')
            data = {'company_id':Comp_ID, 'company_name':company_name,'industry':industry,
                    'size':size, 'direct_link':direct_link}
            data_list.append(data)
        df_comp = pd.DataFrame(data_list)
        return df_comp
    except Exception as error:
        suffix = str(error)
        error_prefix = ErrorHandling.GLASSDOOR_COMPANIES_ERROR.value
        show_error_message(error_prefix, suffix)