from enum import Enum

class glassdoor(Enum):
    link = 'https://www.glassdoor.com/Job/data-engineer-jobs-SRCH_KO0,13.htm?fromAge=1'

class glassdoor_xpaths(Enum):
    XPATH_NUMBER_OF_ELEMENTS = '//*[@id="left-column"]/div[1]/h1'
    XPATH_NEXT_PAGE = '//*[@id="left-column"]/div[2]/div/button'
    XPATH_EXIT_LOGIN = '//*[@id="LoginModal"]/div/div/div/div[2]/button'
    
class glassdoor_classes(Enum):
    CLASS_JOB_TITLE        = 'css-1nh9iuj'
    CLASS_JOB_LOCATION     = 'location'
    CLASS_JOB_COMPANY_NAME = 'css-8wag7x'
    CLASS_JOB_SALARY       = 'salary-estimate'
    CLASS_JOB_DATE         = 'd-flex'

class TAGS(Enum):
    LI = 'li'

class GLASSDOOR_DF(Enum):
    BOARD_COLUMNS_LIST = ['title','company','location','link','salary']

class glassdoor_css_selectors(Enum):
    LI_JOBS_LIST = 'li.JobsList_jobListItem__JBBUV'
    LI_JOB_DATE = '[data-test="job-age"]'

class linkedin_xpaths(Enum):
    JOB_TITLE = '//h3[@class = "base-search-card__title"]'
    COMPANIES = '//a[@class = "hidden-nested-link"]'
    LINKS = '//a[@class = "base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"]'
    POSTING_TIME = '//time[@class = "job-search-card__listdate"]'
    LOCATIONS = '//span[@class = "job-search-card__location"]'

class linkedin_attributes(Enum):
    HREF = 'href'
    DATETIME = 'datetime'

class linkedin_url(Enum):
    url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%2Bengineer&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&start=0'
